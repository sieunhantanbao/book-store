from ... import db_context

class Category(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    name = db_context.Column(db_context.String(1000))
    slug = db_context.Column(db_context.String(1000))
    short_description = db_context.Column(db_context.String(1000))
    thumbnail = db_context.Column(db_context.String(10000))
    sort_order = db_context.Column(db_context.Integer)
    created_at = db_context.Column(db_context.DateTime(timezone = True))
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    books = db_context.relationship('Book', backref='category')