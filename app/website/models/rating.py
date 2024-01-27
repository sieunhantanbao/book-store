from datetime import datetime
from ... import db_context

class Rating(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    user_id = db_context.Column(db_context.Integer, db_context.ForeignKey('user.id'), nullable=False)
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=False)
    rating_value  = db_context.Column(db_context.Float)
    comment = db_context.Column(db_context.String(10000), default = None)
    created_at = db_context.Column(db_context.DateTime(timezone = True), default = datetime.now())
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    is_reviewed = db_context.Column(db_context.Boolean, default = False)
