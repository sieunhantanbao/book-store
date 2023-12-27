from flask import Blueprint, render_template, request, redirect, url_for
from ..models.db_models import User
from werkzeug.security import generate_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user
from ..models.validation_models import ProfileForm, RegistrationForm, LoginForm, ChangePasswordForm
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('dashboard.home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember= True)
            return redirect(url_for('dashboard.home'))
    return render_template('auth/login.html', form=form, user = current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password_hashed = generate_password_hash(form.password.data)
        new_user = User(email = form.email.data, 
                        first_name = form.first_name.data,
                        last_name = form.last_name.data, 
                        password = password_hashed)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember = True)
        return redirect(url_for('dashboard.home'))
    return render_template('auth/register.html', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=current_user.email).first()
        password_hashed = generate_password_hash(form.new_password.data)
        user.password = password_hashed
        db.session.commit()
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('auth/change_password.html', form= form, user = current_user)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(request.form)
    update_message = ''
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=current_user.email).first()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.telephone = request.form.get('telephone')
        user.address = request.form.get('address')
        user.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%m/%d/%Y')
        user.photo =  request.form.get('photo')
        db.session.commit()
        update_message = 'The profile is updated successfully'
    return render_template('auth/profile.html',form = form, user = current_user, message = update_message)
