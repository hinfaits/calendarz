from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, URL

# pylint: disable=too-few-public-methods
class NewForm(FlaskForm):
    """
    This form has fields required for creating new calendar objects
    """
    url = StringField('URL', validators=[DataRequired(), URL(),])
    source_type = RadioField('Source',
                             # choices=[('google_sheets', 'Google Sheets',),
                             #          ('json', 'JSON',),
                             #          ('csv', 'CSV',),],
                             choices=[('json', 'JSON',), ('csv', 'CSV',),],
                             validators=[DataRequired(),])

# pylint: disable=too-few-public-methods
class EditForm(NewForm):
    """
    This form has fields for creating calendar objects and also to
    modify their properties
    """
    name = StringField('name', validators=[DataRequired(),])
