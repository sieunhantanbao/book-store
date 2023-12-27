from .. import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    date_of_birth = db.Column(db.DateTime(timezone=True))
    photo = db.Column(db.String(10000))
    telephone = db.Column(db.String(20))
    address = db.Column(db.String(500))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(10000))
    price = db.Column(db.Float)
    isbn = db.Column(db.String(50))
    author = db.Column(db.String(150))
    publisher = db.Column(db.String(150))
    publish_date = db.Column(db.DateTime(timezone=True))
    pages = db.Column(db.Integer)
    dimensions = db.Column(db.String(150))
    language = db.Column(db.String(50))
    thumbnail = db.Column(db.String(10000))

class WishList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating_value  = db.Column(db.Float)

class BookComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    comment = db.Column(db.String(10000))

