from ... import db_context
from .book_category import Category

class Book(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    title = db_context.Column(db_context.NVARCHAR(1000), nullable=False)
    slug = db_context.Column(db_context.String(1000), nullable=False)
    short_description = db_context.Column(db_context.NVARCHAR(1000))
    description = db_context.Column(db_context.NVARCHAR)
    price = db_context.Column(db_context.Float, nullable=False)
    isbn = db_context.Column(db_context.String(50), nullable=False)
    author = db_context.Column(db_context.NVARCHAR(150), nullable=False)
    publisher = db_context.Column(db_context.NVARCHAR(150))
    publish_date = db_context.Column(db_context.DateTime(timezone=True))
    pages = db_context.Column(db_context.Integer)
    dimensions = db_context.Column(db_context.String(150))
    language = db_context.Column(db_context.NVARCHAR(50))
    thumbnail_url = db_context.Column(db_context.Text)
    sort_order = db_context.Column(db_context.Integer)
    is_featured = db_context.Column(db_context.Boolean, nullable=False, default = False)
    is_published = db_context.Column(db_context.Boolean, nullable=False, default = False)
    created_at = db_context.Column(db_context.DateTime(timezone = True), nullable=False)
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    category_id = db_context.Column(db_context.Integer, db_context.ForeignKey('category.id'), nullable=False)
    ratings = db_context.relationship('Rating', backref='book', lazy=True)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}