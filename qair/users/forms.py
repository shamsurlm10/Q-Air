from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegisterForm(FlaskForm):
    pass

class LoginForm(FlaskForm):
    pass