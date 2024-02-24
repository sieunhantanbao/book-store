from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ...services import book_client_service as _book_service, rating_client_service as _rating_service, wishlist_service as _wishlist_service
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
#@login_required
def home():
    """
    Dashboard page
    """
    books = _book_service.get_all()
    book_average_ratings = _rating_service.get_all_average_rating()
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
        return render_template('client/index.html',
                            books = books,
                            wishlists = wishlists,
                            book_average_ratings = book_average_ratings,
                            user = current_user)
    else:
        return render_template('client/index.html',
                            books = books,
                            book_average_ratings = book_average_ratings,
                            user = None)