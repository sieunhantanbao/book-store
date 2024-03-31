from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask_login import login_required, current_user
from app.database import get_db_context
from app.website.models.constants.constants import REDIS_KEY_CLIENT_LIST_ALL_CATEGORIES, REDIS_KEY_CLIENT_LIST_SHORT_CATEGORIES

from app.website.schemas.category import Category
from app.website.utilities.extensions import clear_redis_cache, is_admin, remove_file
from ...services import book_service as _book_service, image_service as _image_service
from ...models.validations.category_validation import CategoryCreateForm


admin_category = Blueprint('category_controller', __name__)
db = next(get_db_context())

@admin_category.route('/', methods=['GET'])
@login_required
@is_admin
def list() -> list[Category]:
    """Get all categories

    Returns:
        list[Category]: List of category
    """
    if current_user.is_authenticated:
        categories = _book_service.get_all_categories(db)
        return render_template('admin/category_list.html', categories = categories, user = current_user)
    return redirect(url_for('auth.login'))


@admin_category.route('/create', methods=['GET', 'POST'])
@login_required
@is_admin
def create():
    """Create a category

    Returns:
        _type_: _description_
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
@is_admin
def edit_category(cat_id):
    """Edit a category

    Args:
        cat_id (_type_): Category Id

    Returns:
        _type_: _description_
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
@is_admin
def delete_image(image_id):
    """ Delete a category

    Args:
        image_id (_type_): Image Id associated with category to delete

    Returns:
        _type_: _description_
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
