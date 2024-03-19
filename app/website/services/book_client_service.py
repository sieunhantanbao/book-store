from uuid import UUID
from sqlalchemy import desc
from sqlalchemy.orm import Session
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

def get_all(db: Session):
    """
    Get all books
    """
    books = db.query(Book).filter_by(is_published=True).all()
    return books

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

def get_by_cat(db: Session, cat_id: UUID):
    """
    Get all books by the Category
    """
    books = db.query(Book).filter(Book.is_published==True, Book.category_id==cat_id).all()
    return books

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

