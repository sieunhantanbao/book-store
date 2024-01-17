from flask import Blueprint, render_template, request, make_response, jsonify
from flask_login import login_required, current_user
from ...services import book_client_service as _book_service, wishlist_service as _wishlist_service, rating_service as _rating_service
book = Blueprint('book', __name__)

@book.route('/detail/<id_or_slug>')
@login_required
def book_detail(id_or_slug):
    """
    Get a book detail
    """
    book = _book_service.get_by_id(id_or_slug)
    return render_template('client/book_detail.html', book = book, user=current_user)


@book.route('/add-wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    "API to save/add a book to wishlist"
    data = request.json
    result = _wishlist_service.create(current_user.id, data['book_id'])
    return make_response(jsonify(success=result), 200)


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
    books = [result.Book for result in results]
    for book in books:
            if book.thumbnail != None:
                book.thumbnail =  book.thumbnail.decode("utf-8")
    return render_template('client/wishlist.html', books = books ,user = current_user)


@book.route('/add-rating', methods = ['POST'])
@login_required
def add_rating():
    """
    Create a book rating
    """
    data = request.json
    result, average_rating = _rating_service.create_or_update(current_user.id, data['book_id'], data['rating_value'])
    return make_response(jsonify(success = result, average_rating = average_rating), 200)