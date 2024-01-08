import base64
from flask import Request
from app.website.models.validations.auth_validation import ChangePasswordForm, ProfileForm, RegistrationForm
from ..models.user import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from ... import db_context

def get_all():
    """
    Get all users from database
    """
    users = User.query.all()
    for user in users:
        if user.photo != None:
            user.photo =  user.photo.decode("utf-8")
    return users

def get_by_email(email:str):
    """
    Get Active User by Email
    """
    return User.query.filter_by(email=email, is_active=True).first()

def register(form:RegistrationForm):
    """
    Register a new user
    """
    password_hashed = generate_password_hash(form.password.data)
    new_user = User(email = form.email.data, 
                    first_name = form.first_name.data,
                    last_name = form.last_name.data, 
                    password = password_hashed,
                    created_at = datetime.now())
    db_context.session.add(new_user)
    db_context.session.commit()
    return new_user

def change_password(user:User, form:ChangePasswordForm):
    """
    Update user password
    """
    password_hashed = generate_password_hash(form.new_password.data)
    user.password = password_hashed
    user.updated_at = datetime.now()
    db_context.session.commit()

def update(user:User, form:ProfileForm, request:Request):
    """
    Update user profile
    """
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.telephone = request.form.get('telephone')
    user.address = request.form.get('address')
    user.experience_in = request.form.get('experience_in')
    user.addition_detail = request.form.get('addition_detail')
    user.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%m/%d/%Y')
    user.updated_at = datetime.now()
    # Update database
    db_context.session.commit()

def update_profile_photo(user: User, request:Request):
    """
    User user profile photo
    """
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            user.photo = base64.b64encode(uploaded_file.read())
            # Update database
            db_context.session.commit()
    # else donothing
    
    
