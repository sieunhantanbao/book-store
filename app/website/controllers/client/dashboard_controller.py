from flask import Blueprint, render_template
from flask_login import current_user
from app.database import get_db_context
from ...models.constants.constants import NUMBER_OF_BOOKS_HOME_PAGE
from ...services import book_client_service as _book_service, rating_client_service as _rating_service, wishlist_service as _wishlist_service


dashboard = Blueprint('dashboard', __name__)
db = next(get_db_context())

@dashboard.route('/')
def home():
    """ Home page

    Returns:
        _type_: _description_
    """
    books = _book_service.get_with_limit(db, NUMBER_OF_BOOKS_HOME_PAGE)
    book_ids = [book.id for book in books]
    book_average_ratings = _rating_service.get_all_average_rating(db, book_ids)
    for book in books:
        average_rating = [book_average_rating for book_average_rating in book_average_ratings if book_average_rating.book_id == book.id]
        if average_rating:
            book.average_rating_value = average_rating[0].average_rating_value
            book.total_ratings = average_rating[0].total_ratings
        else:
            book.average_rating_value = None
            book.total_ratings = None

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
        return render_template('client/index.html',
                            categories = categories,
                            books = books,
                            wishlists = wishlists,
                            user = current_user)
    else:
        return render_template('client/index.html',
                            categories = categories,
                            books = books,
                            user = None)