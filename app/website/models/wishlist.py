from ... import db_context

class WishList(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    user_id = db_context.Column(db_context.Integer, db_context.ForeignKey('user.id'), nullable=False)
    book_id = db_context.Column(db_context.Integer, db_context.ForeignKey('book.id'), nullable=False)