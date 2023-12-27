from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import ValidationError
from .db_models import User
from werkzeug.security import check_password_hash
from flask_login import current_user

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('This email is already exists')

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('Email is incorrect')
        
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                raise ValidationError('Password is incorrect')

class ChangePasswordForm(Form):
    current_password =  PasswordField('Current Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_new_password', message='Passwords must match')
    ])
    confirm_new_password = PasswordField('Confirm New Password', [validators.DataRequired()])

    def validate_current_password(self, field):
        if not current_user or current_user == None:
            raise ValidationError('You are not logged in yet')
        else:
            user = User.query.filter_by(email=current_user.email).first()
            if user:
                if not check_password_hash(user.password, field.data):
                    raise ValidationError('Current password is incorrect')
            else:
                raise ValidationError('You are not logged in yet')

class ProfileForm(Form):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
