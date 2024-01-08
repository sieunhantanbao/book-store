from ... import db_context

class BookComment(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    user_id = db_context.Column(db_context.Integer, db_context.ForeignKey('user.id'))
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'))
    comment = db_context.Column(db_context.String(10000))
    created_at = db_context.Column(db_context.DateTime(timezone = True))
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)