from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from flask_login import login_user, login_required, logout_user, current_user
from ..models.validations.auth_validation import ProfileForm, RegistrationForm, LoginForm, ChangePasswordForm
from ..services import user_service as _user_service

auth = Blueprint('auth', __name__)

"""
User login
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('dashboard.home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = _user_service.get_by_email(form.email.data)
        if user:
            login_user(user, remember= True)
            returnUrl = request.args.get('next')
            if None != returnUrl:
                return redirect(returnUrl)
            return redirect(url_for('dashboard.home'))
    return render_template('common/auth/login.html', form=form, user = current_user)

"""
Register a new user
"""
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = _user_service.register(form)
        login_user(new_user, remember = True)
        return redirect(url_for('dashboard.home'))
    return render_template('common/auth/register.html', form=form, user=current_user)

"""
Log out
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""
Change password
"""
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = _user_service.get_by_email(current_user.email)
        _user_service.change_password(user, form)
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('common/auth/change_password.html', form= form, user = current_user)

"""
Update user profile
"""
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(request.form)
    update_message = ''
    if request.method == 'POST' and form.validate():
        user = _user_service.get_by_email(current_user.email)
        _user_service.update(user, form, request)
        update_message = 'The profile is updated successfully'
    return render_template('common/auth/profile.html',form = form, user = current_user, message = update_message)

"""
Update user profile photo
"""
@auth.route('/profile/photo', methods=['POST'])
@login_required
def change_profile_photo():
    if current_user.is_authenticated:
        user = _user_service.get_by_email(current_user.email)
        _user_service.update_profile_photo(user, request)
        # Return to client
        return make_response(jsonify(user_photo=user.photo.decode("utf-8")), 200)
    return make_response(jsonify(message='Unauthorized'), 401)