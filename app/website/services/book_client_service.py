from uuid import UUID
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.website.models.dtos.book import BookFilterInputModel
from app.website.schemas.book_relation import BookRelation
from ..utilities.extensions import is_valid_uuid
from ..schemas.book import Book
from ..schemas.category import Category
from ..schemas.wishlist import WishList


def get_by_id(db: Session, id_or_slug):
    is_id = UUID(id_or_slug) if is_valid_uuid(id_or_slug) else False
    if is_id != False:
        return db.query(Book).filter_by(id = is_id, is_published = True).first()
    else:
        return db.query(Book).filter_by(slug = id_or_slug, is_published = True).first()

def get_all(db: Session, filter: BookFilterInputModel):
    """
    Get all books
    """
    query = db.query(Book).filter(Book.is_published == True)
    # Filter by price
    query =  query.filter(Book.price >= filter.min_price_input, Book.price <= filter.max_price_input)
    # Filter by Keyword
    if filter.keyword !='' and filter.keyword != None:
        query = query.filter(Book.title.ilike(f"%{filter.keyword}%"))
    if len(filter.category) > 0:
        query = query.filter(or_(Book.category_id.in_(filter.category)))
    # Order by    
    order_by = desc(Book.created_at)
    match filter.sort_by:
        case 'price_high_low':
            order_by = desc(Book.price)
        case 'price_low_high':
            order_by = asc(Book.price)
        case 'featured':
            order_by = desc(Book.is_featured)
    
    query = query.order_by(order_by)
    # Return data
    return query.all()

def get_with_limit(db: Session, size: int):
    """ Get all books with limit

    Args:
        db (Session): Db Context
        size (int): Number of books

    Returns:
        _type_: _description_
    """
    books = db.query(Book).filter(Book.is_published==True).order_by(desc(Book.created_at)).limit(size).all()
    return books

def get_by_cat(db: Session, cat_id: UUID, size: int = 0, excluded_id: UUID = None):
    """
    Get all books by the Category
    """
    query = db.query(Book).filter(Book.is_published==True, Book.category_id==cat_id)
    if excluded_id != None:
        query = query.filter(Book.id != excluded_id)
    if size != 0:
        return query.limit(size).all()
    return query.all()

def get_all_categories(db: Session, size: int = 0):
    """
    Get Categories from the database
    """
    if size and size > 0:
        return db.query(Category).limit(size).all()
    else:
        return db.query(Category).all()
    
def get_category_by_id(db: Session, id_or_slug):
    is_id = int(id_or_slug) if is_valid_uuid(id_or_slug) else False
    if is_id != False:
        return db.query(Category).filter_by(id = is_id).first()
    else:
        return db.query(Category).filter_by(slug = id_or_slug).first()

    
def get_book_wishlists(db: Session, user_id: UUID):
    """
    Get all my book wishlist
    """
    return db.query(Book, WishList).join(WishList).filter(WishList.user_id==user_id, Book.id==WishList.book_id).all()

def get_featured(db: Session, size: int):
    """
    Get featured books by size
    """
    books = db.query(Book).filter(Book.is_published==True, Book.is_featured==True).order_by(desc(Book.created_at)).limit(size).all()
    return books

def get_related_books(db: Session, book_id: UUID):
    related_books = (
        db.query(Book)
        .join(
            BookRelation,
            or_(
                Book.id == BookRelation.book_id_1,
                Book.id == BookRelation.book_id_2
            )
        )
        .filter(
            or_(
                BookRelation.book_id_1 == book_id,
                BookRelation.book_id_2 == book_id
            ),
            Book.id != book_id
        )
        .all()
    )
    return related_books
