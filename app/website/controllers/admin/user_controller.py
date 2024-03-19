from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.database import get_db_context
from ...services import user_service as _user_service


admin_user = Blueprint('user_controller', __name__)
db = next(get_db_context())

@admin_user.route('/', methods=['GET'])
@login_required
def list():
    if current_user.is_authenticated:
        users = _user_service.get_all(db)
        return render_template('admin/user_list.html', users = users, user = current_user)
    return redirect(url_for('auth.login'))

@admin_user.route('/create', methods=['GET'])
@login_required
def create():
    if current_user.is_authenticated:
        return render_template('admin/user_create.html', user = current_user)
    return redirect(url_for('auth.login'))
