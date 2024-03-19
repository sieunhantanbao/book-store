from uuid import UUID
from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user

from app.database import get_db_context
from ...services import rating_service as _rating_service


admin_rating_review = Blueprint('rating_review_controller', __name__)
db = next(get_db_context())

@admin_rating_review.route('/', methods=['GET'])
@login_required
def list():
    """
    Get all Rating reviews
    """
    if current_user.is_authenticated:
        rating_reviews = _rating_service.get_all_pending_approval(db)
        return render_template('admin/rating_review_list.html', rating_reviews = rating_reviews, user = current_user)
    return redirect(url_for('auth.login'))

@admin_rating_review.route('/approve/<rating_id>', methods=['POST'])
@login_required
def approve(rating_id: UUID, ):
    """
    API to approve a review
    """
    if current_user.is_authenticated:
        success = _rating_service.approve(db, rating_id)
        return make_response(jsonify(success = success), 200)
    return make_response(jsonify(success = False), 401)

@admin_rating_review.route('/delete/<rating_id>', methods=['POST'])
@login_required
def delete(rating_id, ):
    """
    API to approve a review
    """
    if current_user.is_authenticated:
        success = _rating_service.delete(db, rating_id)
        return make_response(jsonify(success = success), 200)
    return make_response(jsonify(success = False), 401)

@admin_rating_review.route('/approve-all/', methods=['POST'])
@login_required
def approve_all():
    """
    API to approve all reviews
    """
    if current_user.is_authenticated:
        success = _rating_service.approve_all(db)
        return make_response(jsonify(success = success), 200)
    return make_response(jsonify(success = False), 401)