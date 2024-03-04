from ... import db_context
from datetime import datetime
class Category(db_context.Model):
    id = db_context.Column(db_context.Integer, primary_key=True)
    name = db_context.Column(db_context.NVARCHAR(1000), nullable=False)
    slug = db_context.Column(db_context.String(1000), nullable=False)
    short_description = db_context.Column(db_context.NVARCHAR(1000))
    thumbnail_url = db_context.Column(db_context.Text)
    sort_order = db_context.Column(db_context.Integer)
    created_at = db_context.Column(db_context.DateTime(timezone = True), nullable=False, default = datetime.now())
    updated_at = db_context.Column(db_context.DateTime(timezone = True), default = None)
    books = db_context.relationship('Book', backref='category', lazy = True)
    images = db_context.relationship('Image', backref='category', lazy = True)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}