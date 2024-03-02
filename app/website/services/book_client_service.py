from sqlalchemy import desc
from ..models.book import Book
from ..models.book_category import Category
from ..models.wishlist import WishList
from ... import db_context

def get_by_id(id_or_slug):
    is_id = int(id_or_slug) if id_or_slug.isdecimal() else False
    if is_id != False:
        return Book.query.filter_by(id = is_id, is_published = True).first()
    else:
        return Book.query.filter_by(slug = id_or_slug, is_published = True).first()

def get_all():
    """
    Get all books
    """
    books = Book.query.filter_by(is_published=True).all()
    return books

def get_all_categories(size: int = 0):
    """
    Get Categories from the database
    """
    if size and size > 0:
        return Category.query.limit(size).all()
    else:
        return Category.query.all()

def get_book_wishlists(user_id):
    """
    Get all my book wishlist
    """
    return db_context.session.query(Book, WishList).join(WishList).filter(WishList.user_id==user_id, Book.id==WishList.book_id).all()

def get_featured(size: int):
    """
    Get featured books by size
    """
    books = Book.query.filter_by(is_published=True, is_featured=True).order_by(desc(Book.created_at)).limit(size).all()
    return books

