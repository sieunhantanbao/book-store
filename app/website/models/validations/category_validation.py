from wtforms import Form, StringField, validators

class CategoryCreateForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    short_description = StringField('Short Description', [validators.DataRequired()])
    