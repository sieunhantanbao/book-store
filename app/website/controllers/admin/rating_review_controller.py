from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask_login import login_required, current_user
from ...services import rating_service as _rating_service
from ...models.validations.book_validation import BookCreateForm

admin_rating_review = Blueprint('rating_review_controller', __name__)


@admin_rating_review.route('/', methods=['GET'])
@login_required
def list():
    """
    Get all Rating reviews
    """
    if current_user.is_authenticated:
        rating_reviews = _rating_service.get_all()
        return render_template('admin/rating_review_list.html', rating_reviews = rating_reviews, user = current_user)
    return redirect(url_for('auth.login'))

# @admin_rating_review.route('/', methods =['GET'])
# @login_required
# def list_pending():
#     """
#     Get all pending for approval ratings
#     """
#     if current_user.is_authenticated:
#         pending_ratings = _rating_service.get_all_pending_approval()
#         return render_template('admin/')
# @admin_rating_review.route('/create', methods=['GET', 'POST'])
# @login_required
# def create():
#     """
#     Create a book
#     """
#     if current_user.is_authenticated:
#         form = BookCreateForm(request.form)
#         publish_date = None
#         categories = _book_service.get_all_categories_for_ddl()
#         if request.method == "POST" and form.validate():
#             publish_date = request.form.get('publish_date')
#             _book_service.create(form, request)
#             return redirect(url_for('book_controller.list')) # seem like this does not affect, the redirect is implemented from the JS (book_create.html)
#         return render_template('admin/book_create.html', form=form, publish_date = publish_date, categories = categories, user=current_user)
#     return redirect(url_for('auth.login'))


# @admin_rating_review.route('/edit/<book_id>', methods=['GET', 'POST'])
# @login_required
# def edit(book_id):
#     """
#     Edit a book
#     """
#     if current_user.is_authenticated:
#         book_to_edit = _book_service.get_by_id(book_id)
#         categories = _book_service.get_all_categories_for_ddl()
#         if request.method == "GET":
#             if book_to_edit:
#                 if book_to_edit.thumbnail != None:
#                     book_to_edit.thumbnail =  book_to_edit.thumbnail.decode("utf-8")
#                 return render_template('admin/book_edit.html', book = book_to_edit, categories=categories, user = current_user)
#         elif request.method == "POST":
#             if book_to_edit:
#                 _book_service.edit(book_to_edit, request)
#             else:
#                 # Error - no book found
#                 return render_template('admin/book_edit.html', book = book_to_edit, categories=categories, user = current_user)
#         return redirect(url_for('book_controller.list'))
#     return redirect(url_for('auth.login'))


# @admin_rating_review.route('/publish/<book_id>/<action>', methods=['PUT'])
# @login_required
# def publish(book_id, action):
#     """
#     Publish/Unpublish a book
#     """
#     if current_user.is_authenticated:
#         book_to_publish = _book_service.get_by_id(book_id)
#         _book_service.publish(book_to_publish, action)
#         return make_response(jsonify(message="Success published/unpublished"), 200)
#     return make_response(jsonify(message="You are not authorized to perform this action."), 401)