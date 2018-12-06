from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CompanySearchForm(FlaskForm):
    """Defines the properties of the form class used to feed
    get input from frontend.
    """
    symbol = StringField('symbol', validators=[DataRequired()])
