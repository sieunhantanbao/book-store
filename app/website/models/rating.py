from datetime import datetime
from ... import db_context

class Rating(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    user_id = db_context.Column(db_context.Integer, db_context.ForeignKey('user.id'), nullable=False)
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=False)
    rating_value  = db_context.Column(db_context.Float, nullable=False)
    comment = db_context.Column(db_context.NVARCHAR, default = None)
    created_at = db_context.Column(db_context.DateTime(timezone = True), nullable=False, default = datetime.now())
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    is_reviewed = db_context.Column(db_context.Boolean, default = False, nullable=False)
