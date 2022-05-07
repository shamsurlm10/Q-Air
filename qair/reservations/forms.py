from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from qair import bcrypt
from qair.models import Flight, User
from wtforms import StringField, RadioField, SelectField, SubmitField, IntegerField
from wtforms.validators import (URL, DataRequired, EqualTo, Length, Optional,
                                ValidationError)


class PaymentForm(FlaskForm):
    flight_class = RadioField('Select the seat class*:', choices=[(0, 'Business Class'), (1, 'Economy Class')], validators=[
        DataRequired()
    ])
    seat_no = SelectField('Seat No*:', choices=[(1, 'A-1'), (2, 'A-2'), (3, 'A-3'),
                                              (4, 'B-1'), (5, 'B-2'), (6, 'B-3'),
                                              (7, 'C-1'), (8, 'C-2'), (9, 'C-3'),
                                              (10, 'D-1'), (11, 'D-2'), (12, 'D-3'), ], validators=[
        DataRequired()
    ])
    trnx_id = StringField("Trnx ID*:", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Trnx ID"})
    submit = SubmitField("Book the Filght")
