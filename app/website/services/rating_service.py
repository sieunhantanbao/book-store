from sqlalchemy import func
from ..models.rating import Rating
from ... import db_context

def get_all(user_id):
    """
    Get all book rating value by user_id
    """
    ratings = Rating.query.filter_by(user_id=user_id).all()
    return ratings

def get_rating_value_by_book_user(user_id, book_id):
    """
    Get Rating value for a book by user_id
    """
    return Rating.query.filter_by(user_id=user_id, book_id=book_id).first()

def get_all_average_rating():
    """
    Get average book ratings
    """
    average_ratings = db_context.session.query(Rating.book_id, func.avg(Rating.rating_value).label('average_rating_value')).group_by(Rating.book_id).all()
    return average_ratings

def get_average_rating_value_by_book(book_id):
    """
    Get average rating for a Book
    """
    return db_context.session.query(func.avg(Rating.rating_value)).filter_by(book_id=book_id).scalar()


def create_or_update(user_id, book_id, rating_value):
    """
    Create a Book rating
    """
    try:
        existing_rating = get_rating_value_by_book_user(user_id, book_id)
        if existing_rating:
            existing_rating.rating_value = rating_value
        else:
            new_rating = Rating(user_id=user_id,
                                book_id=book_id,
                                rating_value=rating_value)
            db_context.session.add(new_rating)
        db_context.session.commit()
        average_rating = get_average_rating_value_by_book(book_id)
        return True, average_rating
    except:
        return False, None