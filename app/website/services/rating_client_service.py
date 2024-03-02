from sqlalchemy import func, desc
from ..models.rating import Rating
from ... import db_context

def get_all(user_id):
    """
    Get all book rating value by user_id
    """
    ratings = Rating.query.filter_by(user_id=user_id, is_reviewed=True).all()
    return ratings

def get_rating_value_by_book_user(user_id, book_id):
    """
    Get Rating value for a book by user_id
    """
    return Rating.query.filter_by(user_id=user_id, book_id=book_id, is_reviewed=True).first()

def get_all_average_rating(book_ids:list):
    """
    Get average book ratings
    """
    average_ratings = db_context.session.query(Rating.book_id, func.avg(Rating.rating_value).label('average_rating_value'), func.count(Rating.book_id).label('total_ratings')).group_by(Rating.book_id).filter(Rating.book_id.in_(book_ids), Rating.is_reviewed).all()
    return average_ratings

def get_average_rating_value_by_book(book_id):
    """
    Get average rating for a Book
    """
    return db_context.session.query(func.avg(Rating.rating_value).label('average_rating_value'), func.count(Rating.book_id).label('total_ratings')).group_by(Rating.book_id).filter_by(book_id=book_id, is_reviewed=True).all()

def get_average_rating_statistic_by_book(book_id):
    """
    Get average rating statistic for a Book
    """
    try:
        data = db_context.session.query(Rating.rating_value, func.count(Rating.user_id).label('total_ratings')).group_by(Rating.rating_value).filter_by(book_id=book_id, is_reviewed=True).all()
        return True, data
    except Exception as e:
        print(e)
        return False, None

def get_book_comments(book_id):
    """
    Get book comments
    """
    # book_comments = db_context.session.query(Rating.book_id, Rating.user_id, Rating.comment, Rating.created_at, Rating.rating_value, Rating.user).filter_by(book_id=book_id, is_reviewed=True).order_by(desc(Rating.created_at)).all()
    book_comments = Rating.query.filter_by(book_id=book_id, is_reviewed=True).order_by(desc(Rating.created_at)).all()
    return book_comments

def create_or_update(user_id, book_id, rating_value, review_comment):
    """
    Add a Book rating
    """
    try:
        new_rating = Rating(user_id=user_id,
                            book_id=book_id,
                            rating_value=rating_value,
                            comment = review_comment,
                            is_reviewed = False)
        
        db_context.session.add(new_rating)
        db_context.session.commit()
        return True
    except Exception as e:
        print(e)
        return False