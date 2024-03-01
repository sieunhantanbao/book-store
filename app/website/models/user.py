from ... import db_context
from datetime import datetime
from flask_login import UserMixin

class User(db_context.Model, UserMixin):
    id = db_context.Column(db_context.Integer, primary_key=True)
    email = db_context.Column(db_context.NVARCHAR(150), unique=True)
    password = db_context.Column(db_context.String(500))
    first_name = db_context.Column(db_context.NVARCHAR(150), nullable=False)
    last_name = db_context.Column(db_context.NVARCHAR(150), nullable=False)
    date_of_birth = db_context.Column(db_context.DateTime(timezone=True))
    photo_url = db_context.Column(db_context.Text)
    telephone = db_context.Column(db_context.String(20))
    address = db_context.Column(db_context.NVARCHAR(500))
    experience_in = db_context.Column(db_context.NVARCHAR)
    addition_detail = db_context.Column(db_context.NVARCHAR)
    is_active = db_context.Column(db_context.Boolean, nullable=False, default = True)
    created_at = db_context.Column(db_context.DateTime(timezone = True), nullable=False, default = datetime.now())
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    ratings = db_context.relationship('Rating', backref='user', lazy=True)