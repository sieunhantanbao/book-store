from ... import db_context
from flask_login import UserMixin

class User(db_context.Model, UserMixin):
    id = db_context.Column(db_context.Integer, primary_key=True)
    email = db_context.Column(db_context.String(150), unique=True)
    password = db_context.Column(db_context.String(150))
    first_name = db_context.Column(db_context.String(150))
    last_name = db_context.Column(db_context.String(150))
    date_of_birth = db_context.Column(db_context.DateTime(timezone=True))
    photo = db_context.Column(db_context.String(10000))
    telephone = db_context.Column(db_context.String(20))
    address = db_context.Column(db_context.String(500))
    experience_in = db_context.Column(db_context.String(5000))
    addition_detail = db_context.Column(db_context.String(5000))
    is_active = db_context.Column(db_context.Boolean, default = True)
    created_at = db_context.Column(db_context.DateTime(timezone = True))
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)