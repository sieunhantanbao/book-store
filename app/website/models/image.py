from ... import db_context
from .book import Book
from .book_category import Category

class Image(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=True)
    category_id = db_context.Column(db_context.Integer, db_context.ForeignKey('category.id'), nullable=True)
    url = db_context.Column(db_context.Text)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}