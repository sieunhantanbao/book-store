from flask import Blueprint, abort, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
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
    # Book thumbnail
    # if book.thumbnail != None:
    #     book.thumbnail =  book.thumbnail.decode("utf-8")
    
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


@book.route('/add-wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    "API to save/add a book to wishlist"
    if current_user and current_user.is_authenticated:
        data = request.json
        result = _wishlist_service.create(current_user.id, data['book_id'])
        return make_response(jsonify(success=result), 200)
    else:
        return make_response(jsonify(success=False), 401)


@book.route('/remove-wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    "API to remove a book from the wishlist"
    data = request.json
    result = _wishlist_service.delete_by_user_and_book(current_user.id, data['book_id'])
    return make_response(jsonify(success=result), 200)


@book.route('/wishlist', methods = ['GET'])
@login_required
def my_book_wishlists():
    """
    Get all my wishlist
    """
    results = _book_service.get_book_wishlists(current_user.id)
    book_average_ratings = _rating_service.get_all_average_rating()
    
    books = [result.Book for result in results]
    for book in books:
        # if book.thumbnail != None:
        #     book.thumbnail =  book.thumbnail.decode("utf-8")
        
        average_rating = [book_average_rating for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
        if average_rating:
            book.average_rating_value = average_rating[0].average_rating_value
            book.total_ratings = average_rating[0].total_ratings
        else:
            book.average_rating_value = None
            book.total_ratings = None
        
    return render_template('client/wishlist.html', books = books ,user = current_user)


@book.route('/add-review', methods = ['POST'])
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
    
@book.route('/star_rating_statistic/<book_id>', methods = ['GET'])
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