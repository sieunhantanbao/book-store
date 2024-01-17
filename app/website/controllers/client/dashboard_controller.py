from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ...services import book_client_service as _book_service, wishlist_service as _wishlist_service, rating_service as _rating_service
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
#@login_required
def home():
    """
    Dashboard page
    """
    if current_user!= None and current_user.is_authenticated:
        categories = _book_service.get_all_categories()
        books = _book_service.get_all()
        featured_books = [book for book in books if book.is_featured]
        wishlists = _wishlist_service.get_all(current_user.id)
        if wishlists:
            wishlists = [wishlist.book_id for wishlist in wishlists]
        book_ratings = _rating_service.get_all(current_user.id)
        book_average_ratings = _rating_service.get_all_average_rating()
        for book in books:
            rating_value = [book_rating.rating_value for book_rating in book_ratings if book_rating.book_id == book.id]
            if rating_value:
                book.rating_value = rating_value[0]
            else:
                book.rating_value = None
            average_rating_value = [book_average_rating.average_rating_value for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
            if average_rating_value:
                book.average_rating_value = average_rating_value[0]
            else:
                book.average_rating_value = None
        return render_template('client/index.html', 
                            featured_books = featured_books,
                            categories = categories,
                            books = books,
                            wishlists = wishlists,
                            book_average_ratings = book_average_ratings,
                            user = current_user)
    else:
        categories = _book_service.get_all_categories()
        books = _book_service.get_all()
        featured_books = [book for book in books if book.is_featured]
        book_average_ratings = _rating_service.get_all_average_rating()
        for book in books:
            book.rating_value = None
            average_rating_value = [book_average_rating.average_rating_value for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
            if average_rating_value:
                book.average_rating_value = average_rating_value[0]
            else:
                book.average_rating_value = None
        return render_template('client/index.html', 
                            featured_books = featured_books,
                            categories = categories,
                            books = books,
                            book_average_ratings = book_average_ratings,
                            user = None)