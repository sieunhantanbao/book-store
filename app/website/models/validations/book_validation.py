from wtforms import Form, StringField, validators, DecimalField, IntegerField

class BookCreateForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    description = StringField('Description', [])
    price = DecimalField('Price', [validators.NumberRange(min=0), validators.DataRequired()])
    isbn = StringField('ISBN', [validators.DataRequired()])
    author = StringField('Author', [validators.DataRequired()])
    publisher = StringField('Publisher', [])
    pages = IntegerField('Total pages', [validators.NumberRange(min=0)])
    dimensions = StringField('Dimensions', [])
    language = StringField('Language', [])
    thumbnail = StringField('Thumbnail', [])