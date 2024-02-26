
from sqlalchemy import desc
from ..models.rating import Rating
from datetime import datetime
from ... import db_context

def get_all():
    """
    Get all ratings and reviews
    """
    rating_reviews = Rating.query.order_by(desc(Rating.created_at)).all()
    return rating_reviews

def get_all_pending_approval():
    """
    Get all pending approval rating comments
    """
    rating_reviews = Rating.query.filter(Rating.is_reviewed==False).order_by(desc(Rating.created_at)).all()
    return rating_reviews

def approve(rating_id):
    """
    Approve a rating review
    """
    rating_to_approve = Rating.query.filter_by(id=rating_id, is_reviewed =False).first()
    if rating_to_approve:
        rating_to_approve.is_reviewed = True
        rating_to_approve.updated_at = datetime.now()
        db_context.session.commit()
        return True
    return False

def approve_all():
    """
    Approve all ratings reviews
    """
    try:
        ratings_to_approve = Rating.query.filter(Rating.is_reviewed == False).all()
        for rating_to_approve in ratings_to_approve:
            rating_to_approve.is_reviewed = True
            rating_to_approve.updated_at = datetime.now()
        db_context.session.commit()
        return True
    except:
        return False

def delete(rating_id):
    """
    Delete a review
    Args:
        rating_id (int): Review Id
    """
    try:
        rating_to_delete = Rating.query.filter(Rating.id == rating_id).first()
        if rating_to_delete:
            db_context.session.delete(rating_to_delete)
            db_context.session.commit()
            return True
        else:
            return False
    except:
        return False
