from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

admin_dashboard = Blueprint('admin_dashboard', __name__)

@admin_dashboard.route('/', methods=['GET', 'POST'])
@login_required
def list():
    """
    Get list
    """
    if current_user.is_authenticated:
         return render_template('admin/dashboard.html', user = current_user)
    return redirect(url_for('auth.login'))