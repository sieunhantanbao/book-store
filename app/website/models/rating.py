from ... import db_context

class Rating(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    user_id = db_context.Column(db_context.Integer, db_context.ForeignKey('user.id'))
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'))
    rating_value  = db_context.Column(db_context.Float)