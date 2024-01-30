from flask import Blueprint, render_template, redirect, request, url_for, jsonify, make_response
from flask_login import login_required, current_user
from ...services import rating_service as _rating_service

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