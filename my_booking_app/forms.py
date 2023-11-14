# forms.py

from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email

class BookingForm(FlaskForm):
    service_types = [('FOOTBALL', 'Football'), ('BASKETBALL', 'Basketball'), ('GOLF', 'Golf'), ('THE CAGE', 'The Cage'), ('LEISURE', 'Leisure')]
    service_type = SelectMultipleField('Service Type', choices=service_types, validators=[DataRequired()])
    date = DateField('Date', validator)
