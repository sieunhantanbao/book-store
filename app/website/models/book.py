from ... import db_context
from .book_category import Category
from .book_comment import BookComment

class Book(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    title = db_context.Column(db_context.String(1000))
    slug = db_context.Column(db_context.String(1000))
    short_description = db_context.Column(db_context.String(1000))
    description = db_context.Column(db_context.String(10000))
    price = db_context.Column(db_context.Float)
    isbn = db_context.Column(db_context.String(50))
    author = db_context.Column(db_context.String(150))
    publisher = db_context.Column(db_context.String(150))
    publish_date = db_context.Column(db_context.DateTime(timezone=True))
    pages = db_context.Column(db_context.Integer)
    dimensions = db_context.Column(db_context.String(150))
    language = db_context.Column(db_context.String(50))
    thumbnail = db_context.Column(db_context.String(10000))
    sort_order = db_context.Column(db_context.Integer)
    is_featured = db_context.Column(db_context.Boolean, default = False)
    is_published = db_context.Column(db_context.Boolean, default = False)
    created_at = db_context.Column(db_context.DateTime(timezone = True))
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    category_id = db_context.Column(db_context.Integer, db_context.ForeignKey('category.id'))
    comments = db_context.relationship('BookComment', backref='book')