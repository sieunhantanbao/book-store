from flask import Request

from app.website.models.validations.book_validation import BookCreateForm
from app.website.models.validations.category_validation import CategoryCreateForm
from ..models.book import Book
from ..models.book_category import Category
from datetime import datetime
import base64
from slugify import slugify
from ... import db_context

def get_by_id(book_id:int):
    return Book.query.get(book_id)

def get_all():
    """
    Get all books from database
    """
    books = Book.query.all()
    for book in books:
            if book.thumbnail != None:
                book.thumbnail =  book.thumbnail.decode("utf-8")
    return books


def create(form:BookCreateForm, request:Request):
    """
    Create a book and save to database
    """
    new_book = Book(title = form.title.data,
                    short_description = form.short_description.data,
                    slug = slugify(form.title.data),
                    price = form.price.data,
                    description = form.description.data,
                    isbn = form.isbn.data,
                    author = form.author.data,
                    publisher = form.publisher.data,
                    pages = form.pages.data,
                    dimensions = form.dimensions.data,
                    language = form.language.data,
                    is_featured = True if request.form.get('is_featured') == 'on' else False,
                    created_at = datetime.now(),
                    category_id = form.category_id.data
                    )
    publish_date = request.form.get('publish_date')
    if publish_date != None and publish_date !='':
        new_book.publish_date = datetime.strptime(publish_date, '%m/%d/%Y')

    if 'file[0]' in request.files:
        uploaded_file = request.files['file[0]']
        if uploaded_file.filename != '':
                new_book.thumbnail = base64.b64encode(uploaded_file.read())
    
    db_context.session.add(new_book)
    db_context.session.commit()

def edit(book_to_edit:Book, request:Request):
    """
    Edit a book
    """
    publish_date = request.form.get('publish_date')
    if publish_date != None and publish_date !='':
            book_to_edit.publish_date = datetime.strptime(publish_date, '%m/%d/%Y')

    if 'file[0]' in request.files:
            uploaded_file = request.files['file[0]']
            if uploaded_file.filename != '':
                book_to_edit.thumbnail = base64.b64encode(uploaded_file.read())

    book_to_edit.title = request.form.get('title')
    book_to_edit.slug = slugify(book_to_edit.title)
    book_to_edit.short_description = request.form.get('short_description')
    book_to_edit.price = request.form.get('price')
    book_to_edit.description = request.form.get('description')
    book_to_edit.isbn = request.form.get('isbn')
    book_to_edit.author = request.form.get('author')
    book_to_edit.publisher = request.form.get('publisher')
    book_to_edit.pages = request.form.get('pages')
    book_to_edit.dimensions = request.form.get('dimensions')
    book_to_edit.language = request.form.get('language')
    book_to_edit.is_featured = True if request.form.get('is_featured')=='on' else False
    book_to_edit.updated_at = datetime.now()
    book_to_edit.category_id = request.form.get('category_id')
    # Update database
    db_context.session.commit()

def publish(book_to_publish:Book, action:str):
    """
    Publish or unpublish a book
    """
    if action.lower() == 'publish':
        book_to_publish.is_published = True
    else:
        book_to_publish.is_published = False
    book_to_publish.updated_at = datetime.now()
    # Update database
    db_context.session.commit()

#######################CATEGORY#############################################
def get_category_by_id(cat_id:int):
    return Category.query.get(cat_id)


def get_all_categories():
    """
    Get all categories
    """
    categories = Category.query.all()
    for category in categories:
            if category.thumbnail != None and category.thumbnail != '':
                category.thumbnail =  category.thumbnail.decode("utf-8")
    return categories

def get_all_categories_for_ddl():
    """
    Get all categories for dropdownlist
    """
    categories = db_context.session.query(Category.id, Category.name).options(db_context.undefer('*')).all()
    return categories

def create_category(form:CategoryCreateForm, request:Request):
    """
    Create a Category and save to database
    """
    new_category = Category(name = form.name.data,
                    short_description = form.short_description.data,
                    slug = slugify(form.name.data),
                    created_at = datetime.now())

    if 'file[0]' in request.files:
        uploaded_file = request.files['file[0]']
        if uploaded_file.filename != '':
                new_category.thumbnail = base64.b64encode(uploaded_file.read())
    
    db_context.session.add(new_category)
    db_context.session.commit()

def edit_category(category_to_edit:Category, request:Request):
    """
    Edit a Category
    """
    if 'file[0]' in request.files:
            uploaded_file = request.files['file[0]']
            if uploaded_file.filename != '':
                category_to_edit.thumbnail = base64.b64encode(uploaded_file.read())
    category_to_edit.name = request.form.get('name')
    category_to_edit.slug = slugify(category_to_edit.name)
    category_to_edit.short_description = request.form.get('short_description')
    category_to_edit.updated_at = datetime.now()
    # Update database
    db_context.session.commit()