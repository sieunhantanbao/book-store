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
    Get all books from database
    """
    books = Book.query.filter_by(is_published=True).all()
    for book in books:
            if book.thumbnail != None:
                book.thumbnail =  book.thumbnail.decode("utf-8")
    return books

def get_all_categories():
    """
    Get all categories
    """
    categories = Category.query.all()
    for category in categories:
            if category.thumbnail != None and category.thumbnail != '':
                category.thumbnail =  category.thumbnail.decode("utf-8")
    return categories

def get_book_wishlists(user_id):
    """
    Get all my book wishlist
    """
    return db_context.session.query(Book, WishList).join(WishList).filter(WishList.user_id==user_id, Book.id==WishList.book_id).all()
