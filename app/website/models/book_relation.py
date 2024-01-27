from ... import db_context
from .book_category import Book

class BookRelation(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    book_id_1 = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=False)
    book_id_2 = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=False)