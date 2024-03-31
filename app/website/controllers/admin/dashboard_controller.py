from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.website.utilities.extensions import is_admin

admin_dashboard = Blueprint('admin_dashboard', __name__)

@admin_dashboard.route('/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_dasboard():
     """ Admin dashboard page

     Returns:
         _type_: _description_
     """
     if current_user.is_authenticated:
          return render_template('admin/dashboard.html', user = current_user)
     return redirect(url_for('auth.login'))