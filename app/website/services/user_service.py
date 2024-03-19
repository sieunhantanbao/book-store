from flask import Request
from app.website.models.validations.auth_validation import ChangePasswordForm, ProfileForm, RegistrationForm
from app.website.utilities.extensions import allowed_file, upload_file
from ..schemas.user import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import Session


def get_all(db: Session):
    """
    Get all users from database
    """
    users = db.query(User).all()
    return users

def get_by_email(db: Session, email:str):
    """
    Get Active User by Email
    """
    return db.query(User).filter_by(email=email, is_active=True).first()

def register(db: Session, form:RegistrationForm):
    """
    Register a new user
    """
    password_hashed = generate_password_hash(form.password.data)
    new_user = User(email = form.email.data, 
                    first_name = form.first_name.data,
                    last_name = form.last_name.data, 
                    password = password_hashed,
                    created_at = datetime.now())
    db.add(new_user)
    db.commit()
    return new_user

def change_password(db: Session, user:User, form:ChangePasswordForm):
    """
    Update user password
    """
    password_hashed = generate_password_hash(form.new_password.data)
    user.password = password_hashed
    user.updated_at = datetime.now()
    db.commit()

def update(db: Session, user:User, form:ProfileForm, request:Request):
    """
    Update user profile
    """
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.telephone = request.form.get('telephone')
    user.address = request.form.get('address')
    user.experience_in = request.form.get('experience_in')
    user.addition_detail = request.form.get('addition_detail')
    if request.form.get('date_of_birth'):
        user.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%m/%d/%Y')
    user.updated_at = datetime.now()
    # Update database
    db.commit()

def update_profile_photo(db: Session, user: User, request:Request):
    """
    User user profile photo
    """
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
            file_name = upload_file(uploaded_file)
            user.photo_url = file_name
            # Update database
            db.commit()
    # else donothing
    
    
