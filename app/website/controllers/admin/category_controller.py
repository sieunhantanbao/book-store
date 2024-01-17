from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask_login import login_required, current_user
from ...services import book_service as _book_service
from ...models.validations.category_validation import CategoryCreateForm

admin_category = Blueprint('category_controller', __name__)

@admin_category.route('/', methods=['GET'])
@login_required
def list():
    """
    Get all categories
    """
    if current_user.is_authenticated:
        categories = _book_service.get_all_categories()
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
            _book_service.create_category(form, request)
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
        category_to_edit = _book_service.get_category_by_id(cat_id)
        if request.method == "GET":
            if category_to_edit:
                if category_to_edit.thumbnail != None:
                    category_to_edit.thumbnail =  category_to_edit.thumbnail.decode("utf-8")
                return render_template('admin/category_edit.html', category = category_to_edit, user = current_user)
        elif request.method == "POST":
            if category_to_edit:
                _book_service.edit_category(category_to_edit, request)
            else:
                # Error - no category found
                return render_template('admin/category_edit.html', category = category_to_edit, user = current_user)
        return redirect(url_for('category_controller.list'))
    return redirect(url_for('auth.login'))