from ... import db_context

class Book(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    title = db_context.Column(db_context.String(500))
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
    is_published = db_context.Column(db_context.Boolean, default = False)
    created_at = db_context.Column(db_context.DateTime(timezone = True))
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)