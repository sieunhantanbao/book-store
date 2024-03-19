from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask.json import dump
from flask_login import login_required, current_user
from app.database import get_db_context
from app.website.models.constants.constants import REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES, REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES

from app.website.utilities.extensions import clear_redis_cache, remove_file
from ...services import book_service as _book_service, image_service as _image_service
from ...models.validations.category_validation import CategoryCreateForm


admin_category = Blueprint('category_controller', __name__)
db = next(get_db_context())

@admin_category.route('/', methods=['GET'])
@login_required
def list():
    """
    Get all categories
    """
    if current_user.is_authenticated:
        categories = _book_service.get_all_categories(db)
        return render_template('admin/category_list.html', categories = categories, user = current_user)
    return redirect(url_for('auth.login'))


@admin_category.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    Create a Category
    """
    if current_user.is_authenticated:
        form = CategoryCreateForm(request.form)
        if request.method == "POST" and form.validate():
            _book_service.create_category(db, form, request)
            cache_keys = [REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES, REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES]
            clear_redis_cache(cache_keys)
            return redirect(url_for('category_controller.list'))
        return render_template('admin/category_create.html', form=form, user=current_user)
    return redirect(url_for('auth.login'))


@admin_category.route('/edit/<cat_id>', methods=['GET', 'POST'])
@login_required
def edit_category(cat_id):
    """
    Edit a category
    """
    if current_user.is_authenticated:
        category_to_edit = _book_service.get_category_by_id(db, cat_id)
        if request.method == "GET":
            if category_to_edit:
                return render_template('admin/category_edit.html', category = category_to_edit, user = current_user)
        elif request.method == "POST":
            if category_to_edit:
                _book_service.edit_category(db, category_to_edit, request)
                cache_keys = [REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES, REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES]
                clear_redis_cache(cache_keys)
            else:
                # Error - no category found
                return render_template('admin/category_edit.html', category = category_to_edit, user = current_user)
        return redirect(url_for('category_controller.list'))
    return redirect(url_for('auth.login'))


@admin_category.route('/api/image/remove/<image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    """
    Delete an Image by Id
    """
    if current_user and current_user.is_authenticated:
        result, file_name = _image_service.delete(db, image_id)
        if result:
            # Remove the physical file
            remove_file(file_name)
            return make_response(jsonify(success=result), 200)
        else:
            return make_response(jsonify(success=result), 500)
    else:
        return make_response(jsonify(success=False), 401)
