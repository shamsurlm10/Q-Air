from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, BooleanField, PasswordField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
from qair.models import User


class RegisterForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Email"})
    
    passport = StringField("Passport", validators=[
        DataRequired()], render_kw={"placeholder": "Passport Number"})
    
    full_name = StringField("Full Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Full Name"})
    
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Password"})
    
    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Confirm Password"})
    
    condition_check = BooleanField("Accept terms and conditions")
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Email"})
    
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)],
                             render_kw={"placeholder": "Password"})
    
    remember_me = BooleanField("Remember Me")
    
    submit = SubmitField("Login")
    
class ForgetPasswordForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150), Email()
    ], render_kw={"placeholder": "Enter your associated email address"})
    submit = SubmitField("Send Email")

    def validate_email(self, email: str):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email is not valid. Try another one.")
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type a new password"})
    c_password = PasswordField("Retype Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Retype the password"})
    submit = SubmitField("Change Password")