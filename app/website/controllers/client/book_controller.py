from flask import Blueprint, abort, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
from app import redis_client
import json
from app.database import get_db_context
from app.website.models.constants import constants
from sqlalchemy.orm import Session
from app.website.models.dtos.book import BookFilterInputModel
from app.website.schemas.book import Book

from ...services import book_client_service as _book_service, rating_client_service as _rating_service, wishlist_service as _wishlist_service
book = Blueprint('book', __name__)
db = next(get_db_context())

@book.route('/detail/<id_or_slug>')
def book_detail(id_or_slug):
    """ Get a book detail

    Args:
        id_or_slug (_type_): Id of slug of the book

    Returns:
        _type_: _description_
    """
    book = _book_service.get_by_id(db, id_or_slug)
    if not book:
        abort(404)
    
    # Book average rating
    average_rating = _rating_service.get_average_rating_value_by_book(db, book.id)
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
        book_wishlist = _wishlist_service.get_by_user_and_book(db, current_user.id, book.id)
        if book_wishlist:
            book.in_wishlist = True
        else:
            book.in_wishlist = False
    
    # Rating statistic
    _, data = __get_star_rating_statistic(db, book.id)

    # Book comments
    book_comments = _rating_service.get_book_comments(db, book.id)
    
    # Book in the same category
    books_in_cat = _book_service.get_books_by_cat(db, book.category_id, constants.NUMBER_OF_BOOK_IN_THE_SAME_CAT_BOOK_DETAIL_PAGE, book.id)
    __build_book_ratings(books_in_cat)
    # Book related
    related_books = _book_service.get_related_books(db, book.id)
    __build_book_ratings(related_books)
            
    # Book wishlist        
    if current_user!= None and current_user.is_authenticated:
        wishlists = _wishlist_service.get_all(db, current_user.id)
        if wishlists:
            wishlists = [wishlist.book_id for wishlist in wishlists]
            return render_template('client/book_detail.html', 
                           book = book,
                           books_in_cat = books_in_cat,
                           wishlists = wishlists,
                           rating_statistic = data,
                           book_comments = book_comments,
                           related_books = related_books,
                           user=current_user)
    
    return render_template('client/book_detail.html', 
                           book = book,
                           books_in_cat = books_in_cat,
                           rating_statistic = data,
                           book_comments = book_comments,
                           related_books = related_books,
                           user=current_user)

@book.route('/list')
def book_list():
    """ Get all books with filtering

    Returns:
        _type_: _description_
    """
    # Create an instance of BookFilterInputModel
    filter = BookFilterInputModel(
        keyword=request.args.get('keyword'),
        category=request.args.getlist('category'),
        min_price_input=float(request.args.get('min_price_input', 0)),
        max_price_input=float(request.args.get('max_price_input')),
        min_rate_input=int(request.args.get('min_rate_input', 0)),
        max_rate_input=int(request.args.get('max_rate_input', 5)),
        sort_by=request.args.get('sort_by')
    )
    
    books = _book_service.get_all(db, filter)
    __build_book_ratings(books)
    # Filter by rating
    books = [book for book in books if book.average_rating_value >= filter.min_rate_input and book.average_rating_value <= filter.max_rate_input]
    
    # Sort by rating
    sort_by = True if filter.sort_by == "good_rating" else False
    if sort_by:
        books.sort(key=lambda x: x.average_rating_value, reverse=True)
            
    categories = _book_service.get_all_categories(db)
    for category in categories:
        if category.images and category.images[0] is not None:
            category.thumbnail_url = category.images[0].url
        else:
            category.thumbnail_url = None
        
    if current_user!= None and current_user.is_authenticated:
        wishlists = _wishlist_service.get_all(db, current_user.id)
        if wishlists:
            wishlists = [wishlist.book_id for wishlist in wishlists]
        return render_template('client/book.html',
                            categories = categories,
                            books = books,
                            wishlists = wishlists,
                            user = current_user)
    else:
        return render_template('client/book.html',
                            categories = categories,
                            books = books,
                            user = None)


@book.route('/wishlist', methods = ['GET'])
@login_required
def my_book_wishlist():
    """ Get book's wishlist

    Returns:
        _type_: _description_
    """
    results = _book_service.get_book_wishlists(db, current_user.id)
    books = [result.Book for result in results]
    __build_book_ratings(books)
        
    return render_template('client/wishlist.html', books = books ,user = current_user)

@book.route('/categories/all', methods = ['GET'])
def all_categories():
    """ Get all categories
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
     
    return render_template('client/category.html', user = current_user)

@book.route('/categories/<id_or_slug>', methods = ['GET'])
def category_detail(id_or_slug):
    """ Get category detail by Id or slug

    Args:
        id_or_slug (_type_): Id of slug of the category

    Returns:
        _type_: _description_
    """
    category = _book_service.get_category_by_id(db, id_or_slug)
    if not category:
        abort(404)
        
    books = _book_service.get_books_by_cat(db, category.id)
    __build_book_ratings(books)
    
    if current_user!= None and current_user.is_authenticated:
        wishlists = _wishlist_service.get_all(db, current_user.id)
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
        
def __build_book_ratings(books: list[Book]):
    book_ids = [book.id for book in books]
    book_average_ratings = _rating_service.get_all_average_rating(db, book_ids)
    for book in books:
        book_average_rating = [book_average_rating for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
        if book_average_rating:
            book.average_rating_value = book_average_rating[0].average_rating_value
            book.total_ratings = book_average_rating[0].total_ratings
        else:
            book.average_rating_value = None
            book.total_ratings = None
############### APIs ##################################
@book.route('/api/add-wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    """ Add to wishlist

    Returns:
        _type_: _description_
    """
    if current_user and current_user.is_authenticated:
        data = request.json
        result = _wishlist_service.create(db, current_user.id, data['book_id'])
        return make_response(jsonify(success=result), 200)
    else:
        return make_response(jsonify(success=False), 401)


@book.route('/api/remove-wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    """ API to remove a wishlist

    Returns:
        _type_: _description_
    """
    data = request.json
    result = _wishlist_service.delete_by_user_and_book(db, current_user.id, data['book_id'])
    return make_response(jsonify(success=result), 200)

@book.route('/api/add-review', methods = ['POST'])
@login_required
def add_rating_review():
    """ Create a book rating

    Returns:
        _type_: _description_
    """
    if current_user and current_user.is_authenticated:
        data = request.json
        result = _rating_service.create_or_update(db, current_user.id, data['book_id'], data['rating_value'], data["review_comment"])
        return make_response(jsonify(success = result), 200)
    else:
        return make_response(jsonify(success = False), 401)
    
@book.route('/api/star_rating_statistic/<book_id>', methods = ['GET'])
def get_star_rating_statistic(book_id):
    """API Get Book Star Rating statistic

    Args:
        book_id (_type_): Book id

    Returns:
        _type_: _description_
    """
    success, data = __get_star_rating_statistic(db, book_id)
    return make_response(jsonify(success = success, data = data), 200)

def __get_star_rating_statistic(db: Session, book_id):
    """
    Private method to get the star rating statistic for a book
    """
    success, results = _rating_service.get_average_rating_statistic_by_book(db, book_id)
    average_rating = _rating_service.get_average_rating_value_by_book(db, book_id)
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
    """ API Get All Categories with Redis cache

    Returns:
        _type_: _description_
    """
    get_full = request.args.get('all')
    if get_full != None and get_full == 'False':
        # Get first 6 categories
        serialized_categories_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES)
        if serialized_categories_cached == None:
            categories = _book_service.get_all_categories(db, constants.NUMBER_OF_CATEGORIES_ON_HOME_PAGE)
            for category in categories:
                if category.images and category.images[0] is not None:
                    category.thumbnail_url = category.images[0].url
                else:
                    category.thumbnail_url = None
            categories_dic = [category.as_dict() for category in categories]
            serialized_categories_list = json.dumps(categories_dic)
            redis_client.set(constants.REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES, serialized_categories_list)
            serialized_categories_cached = serialized_categories_list
    else:
        # Get full categories
        serialized_categories_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES)
        if serialized_categories_cached == None:
            categories = _book_service.get_all_categories(db)
            for category in categories:
                if category.images and category.images[0] is not None:
                    category.thumbnail_url = category.images[0].url
                else:
                    category.thumbnail_url = None
            categories_dic = [category.as_dict() for category in categories]
            serialized_categories_list = json.dumps(categories_dic)
            redis_client.set(constants.REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES, serialized_categories_list)
            serialized_categories_cached = serialized_categories_list
    
    return make_response(jsonify(json.loads(serialized_categories_cached)), 200)


@book.route('/api/featured-books', methods = ['GET'])
def get_featured_books():
    """ API Get 10 latest featured books with Redis cache

    Returns:
        _type_: _description_
    """
    serialized_featured_books_cached = redis_client.get(constants.REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS)
    if serialized_featured_books_cached == None:
        featured_books = _book_service.get_featured(db, constants.NUMBER_OF_FEATURED_CAROUSEL)
        for featured_book in featured_books:
            featured_book.thumbnail_url = featured_book.images[0].url if featured_book.images[0] !=None else None
        featured_books_dic = [book.as_dict() for book in featured_books]
        serialized_featured_books_list = json.dumps(featured_books_dic)
        redis_client.set(constants.REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS, serialized_featured_books_list)
        serialized_featured_books_cached = serialized_featured_books_list
    return make_response(jsonify(json.loads(serialized_featured_books_cached)), 200)
############### END APIs ##############################