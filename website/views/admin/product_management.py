from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

admin_product = Blueprint('product_management', __name__)

@admin_product.route('/', methods=['GET', 'POST'])
@login_required
def list():
    if current_user.is_authenticated:
         return render_template('admin/product_list.html', user = current_user)
    return redirect(url_for('auth.login'))


@admin_product.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_authenticated:
         return render_template('admin/product_create.html')
    return redirect(url_for('auth.login'))
