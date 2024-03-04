from flask import Blueprint, abort, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
from app import redis_client
import json
from app.website.models.constants import constants

from ...services import book_client_service as _book_service, rating_client_service as _rating_service, wishlist_service as _wishlist_service
book = Blueprint('book', __name__)

@book.route('/detail/<id_or_slug>')
def book_detail(id_or_slug):
    """
    Get a book detail
    """
    book = _book_service.get_by_id(id_or_slug)
    if not book:
        abort(404)
    
    # Book average rating
    average_rating = _rating_service.get_average_rating_value_by_book(book.id)
    if average_rating:
        book.average_rating_value = average_rating[0].average_rating_value
        book.total_ratings = average_rating[0].total_ratings
    else:
        book.average_rating_value = None
        book.total_ratings = None

    # Book wishlist
    if not current_user.is_authenticated:
        book.in_wishlist = False
    else:
        book_wishlist = _wishlist_service.get_by_user_and_book(current_user.id, book.id)
        if book_wishlist:
            book.in_wishlist = True
        else:
            book.in_wishlist = False
    
    # Rating statistic
    _, data = __get_star_rating_statistic(book.id)

    # Book comments
    book_comments = _rating_service.get_book_comments(book.id)

    return render_template('client/book_detail.html', book = book, rating_statistic = data, book_comments = book_comments, user=current_user)

@book.route('/wishlist', methods = ['GET'])
@login_required
def my_book_wishlists():
    """
    Get all my wishlist
    """
    results = _book_service.get_book_wishlists(current_user.id)
    books = [result.Book for result in results]
    book_ids = [book.id for book in books]
    book_average_ratings = _rating_service.get_all_average_rating(book_ids)
    for book in books:
        average_rating = [book_average_rating for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
        if average_rating:
            book.average_rating_value = average_rating[0].average_rating_value
            book.total_ratings = average_rating[0].total_ratings
        else:
            book.average_rating_value = None
            book.total_ratings = None
        
    return render_template('client/wishlist.html', books = books ,user = current_user)

@book.route('/categories/all', methods = ['GET'])
def all_categories():
    """
    Get all book categories
    """        
    return render_template('client/category.html', user = current_user)

@book.route('/categories/<id_or_slug>', methods = ['GET'])
def category_detail(id_or_slug):
    """
    Get the category detail by id or slug
    """
    category = _book_service.get_category_by_id(id_or_slug)
    if not category:
        abort(404)
        
    books = _book_service.get_by_cat(category.id)
    book_ids = [book.id for book in books]
    book_average_ratings = _rating_service.get_all_average_rating(book_ids)
    for book in books:
        average_rating = [book_average_rating for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
        if average_rating:
            book.average_rating_value = average_rating[0].average_rating_value
            book.total_ratings = average_rating[0].total_ratings
        else:
            book.average_rating_value = None
            book.total_ratings = None
    
    if current_user!= None and current_user.is_authenticated:
        wishlists = _wishlist_service.get_all(current_user.id)
        if wishlists:
            wishlists = [wishlist.book_id for wishlist in wishlists]
        return render_template('client/category_detail.html',
                            category = category,
                            books = books,
                            wishlists = wishlists,
                            user = current_user)
    else:
        return render_template('client/category_detail.html',
                            category = category,
                            books = books,
                            user = None)
############### APIs ##################################
@book.route('/api/add-wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    "API to save/add a book to wishlist"
    if current_user and current_user.is_authenticated:
        data = request.json
        result = _wishlist_service.create(current_user.id, data['book_id'])
        return make_response(jsonify(success=result), 200)
    else:
        return make_response(jsonify(success=False), 401)


@book.route('/api/remove-wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    "API to remove a book from the wishlist"
    data = request.json
    result = _wishlist_service.delete_by_user_and_book(current_user.id, data['book_id'])
    return make_response(jsonify(success=result), 200)

@book.route('/api/add-review', methods = ['POST'])
@login_required
def add_rating_review():
    """
    Create a book rating and review
    """
    if current_user and current_user.is_authenticated:
        data = request.json
        result = _rating_service.create_or_update(current_user.id, data['book_id'], data['rating_value'], data["review_comment"])
        return make_response(jsonify(success = result), 200)
    else:
        return make_response(jsonify(success = False), 401)
    
@book.route('/api/star_rating_statistic/<book_id>', methods = ['GET'])
def get_star_rating_statistic(book_id):
    """
    API Get Book Star Rating statistic
    """
    success, data = __get_star_rating_statistic(book_id)
    return make_response(jsonify(success = success, data = data), 200)

def __get_star_rating_statistic(book_id):
    """
    Private method to get the star rating statistic for a book
    """
    success, results = _rating_service.get_average_rating_statistic_by_book(book_id)
    average_rating = _rating_service.get_average_rating_value_by_book(book_id)
    data = {
        'total_rating_1': 0,
        'total_rating_2': 0,
        'total_rating_3': 0,
        'total_rating_4': 0,
        'total_rating_5': 0,
        'total_ratings': 0,
        'average_rating': average_rating[0].average_rating_value if average_rating else 0
    }

    for result in results:
        data['total_ratings']+= result.total_ratings
        if result.rating_value == 1.0:
            data['total_rating_1'] = result.total_ratings
        elif result.rating_value == 2.0:
            data['total_rating_2'] = result.total_ratings
        elif result.rating_value == 3.0:
            data['total_rating_3'] = result.total_ratings
        elif result.rating_value == 4.0:
            data['total_rating_4'] = result.total_ratings
        elif result.rating_value == 5.0:
            data['total_rating_5'] = result.total_ratings
    return success, data

@book.route('/api/categories', methods = ['GET'])
def get_categories():
    """
    API Get All Categories with Redis cache
    """
    get_full = request.args.get('all')
    if get_full != None and get_full == 'False':
        # Get first 6 categories
        serialized_categories_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES)
        if serialized_categories_cached == None:
            categories = _book_service.get_all_categories(constants.NUMBER_OF_CATEGORIES_ON_HOME_PAGE)
            for category in categories:
                category.thumbnail_url = category.images[0].url if category.images[0] !=None else None
            categories_dic = [category.as_dict() for category in categories]
            serialized_categories_list = json.dumps(categories_dic)
            redis_client.set(constants.REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES, serialized_categories_list)
            serialized_categories_cached = serialized_categories_list
    else:
        # Get full categories
        serialized_categories_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES)
        if serialized_categories_cached == None:
            categories = _book_service.get_all_categories()
            for category in categories:
                category.thumbnail_url = category.images[0].url if category.images[0] !=None else None
            categories_dic = [category.as_dict() for category in categories]
            serialized_categories_list = json.dumps(categories_dic)
            redis_client.set(constants.REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES, serialized_categories_list)
            serialized_categories_cached = serialized_categories_list
    
    return make_response(jsonify(json.loads(serialized_categories_cached)), 200)


@book.route('/api/featured-books', methods = ['GET'])
def get_featured_books():
    """
    API Get 10 latest featured books with Redis cache
    """
    serialized_featured_books_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS)
    if serialized_featured_books_cached == None:
        featured_books = _book_service.get_featured(constants.NUMBER_OF_FEATURED_CAROUSEL)
        for featured_book in featured_books:
            featured_book.thumbnail_url = featured_book.images[0].url if featured_book.images[0] !=None else None
        featured_books_dic = [book.as_dict() for book in featured_books]
        serialized_featured_books_list = json.dumps(featured_books_dic)
        redis_client.set(constants.REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS, serialized_featured_books_list)
        serialized_featured_books_cached = serialized_featured_books_list
    return make_response(jsonify(json.loads(serialized_featured_books_cached)), 200)
############### END APIs ##############################