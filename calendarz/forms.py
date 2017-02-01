from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, URL

class NewForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(),])
    source_type = RadioField('Source',
                              # choices=[('google_sheets', 'Google Sheets',), ('json', 'JSON',), ('csv', 'CSV',),],
                              choices=[('json', 'JSON',), ('csv', 'CSV',),],
                              validators=[DataRequired(),])

class EditForm(NewForm):
    name = StringField('name', validators=[DataRequired(),])
