from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask_login import login_required, current_user
from app.database import get_db_context
from app.website.models.constants.constants import REDIS_KEY_CLIENT_LIST_ALL_BOOKS, REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS

from app.website.utilities.extensions import clear_redis_cache, is_admin
from ...services import book_service as _book_service
from ...models.validations.book_validation import BookCreateForm

admin_book = Blueprint('book_controller', __name__)
db = next(get_db_context())

@admin_book.route('/', methods=['GET'])
@login_required
@is_admin
def list():
    """ Get all books

    Returns:
        _type_: _description_
    """
    if current_user.is_authenticated:
        books = _book_service.get_all(db)
        return render_template('admin/book_list.html', books = books, user = current_user)
    return redirect(url_for('auth.login'))


@admin_book.route('/create', methods=['GET', 'POST'])
@login_required
@is_admin
def create():
    """Create a new book

    Returns:
        _type_: _description_
    """
    if current_user.is_authenticated:
        form = BookCreateForm(request.form)
        publish_date = None
        categories = _book_service.get_all_categories_for_ddl(db)
        if request.method == "POST" and form.validate():
            publish_date = request.form.get('publish_date')
            _book_service.create(db, form, request)
            cache_keys = [REDIS_KEY_CLIENT_LIST_ALL_BOOKS, REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS]
            clear_redis_cache(cache_keys)
            return redirect(url_for('book_controller.list')) # seem like this does not affect, the redirect is implemented from the JS (book_create.html)
        return render_template('admin/book_create.html', form=form, publish_date = publish_date, categories = categories, user=current_user)
    return redirect(url_for('auth.login'))


@admin_book.route('/edit/<book_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def edit(book_id):
    """Edit a book
    TODO: This should be updated to bind the request to the DTO
    Args:
        book_id (_type_): Book Id to edit

    Returns:
        _type_: _description_
    """
    if current_user.is_authenticated:
        book_to_edit = _book_service.get_by_id(db, book_id)
        categories = _book_service.get_all_categories_for_ddl(db)
        if request.method == "GET":
            if book_to_edit:
                return render_template('admin/book_edit.html', book = book_to_edit, categories=categories, user = current_user)
        elif request.method == "POST":
            if book_to_edit:
                _book_service.edit(db, book_to_edit, request)
                cache_keys = [REDIS_KEY_CLIENT_LIST_ALL_BOOKS, REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS]
                clear_redis_cache(cache_keys)
            else:
                # Error - no book found
                return render_template('admin/book_edit.html', book = book_to_edit, categories=categories, user = current_user)
        return redirect(url_for('book_controller.list'))
    return redirect(url_for('auth.login'))


@admin_book.route('/publish/<book_id>/<action>', methods=['PUT'])
@login_required
@is_admin
def publish(book_id, action):
    """ Publish a book

    Args:
        book_id (_type_): Book id
        action (_type_): Action type: publish

    Returns:
        _type_: _description_
    """
    if current_user.is_authenticated:
        book_to_publish = _book_service.get_by_id(db, book_id)
        _book_service.publish(db, book_to_publish, action)
        cache_keys = [REDIS_KEY_CLIENT_LIST_ALL_BOOKS, REDIS_KEY_CLIENT_LIST_FEATURED_BOOKS]
        clear_redis_cache(cache_keys)
        return make_response(jsonify(message="Success published/unpublished"), 200)
    return make_response(jsonify(message="You are not authorized to perform this action."), 401)


