from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from qair import bcrypt
from qair.models import User
from wtforms import (DateField, PasswordField, StringField, SubmitField,
                     IntegerField)
from wtforms.validators import (URL, DataRequired, EqualTo, Length, Optional,
                                ValidationError)


class ProfileInfoForm(FlaskForm):
    full_name = StringField("Full Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Full Name"})
    dob = DateField("Date of Birth", validators=[
        DataRequired()])
    passport_no = StringField("Passport Number", validators=[
        Length(max=17)
    ], render_kw={"placeholder": "Passport Number"})
    contact_no = StringField("Contact Number", validators=[
        Length(max=11)
    ], render_kw={"placeholder": "Contact Number"})
    street = StringField("Street", validators=[
        Length(max=17)
    ], render_kw={"placeholder": "Street Address"})
    postal_code = IntegerField("Postal Code", render_kw={"placeholder": "Postal Code"})
    city = StringField("City", validators=[
        Length(max=10)
    ], render_kw={"placeholder": "City"})
    country = StringField("Country", validators=[
        Length(max=17)
    ], render_kw={"placeholder": "Country Name"})
    
    update = SubmitField("Update")

class ChangePhoto(FlaskForm):
    cover_photo = FileField("Cover Photo", validators=[
                            FileAllowed(["jpg", "jpeg", "png"])])
    profile_photo = FileField("Profile Photo", validators=[
                              FileAllowed(["jpg", "jpeg", "png"])])
    save = SubmitField("Update")
    
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type your old password"})

    new_password = PasswordField("New Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type a new password"})

    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "new_password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Retype the password"})

    save = SubmitField("Update")

    def validate_old_password(self, old_password):
        user = User.query.get(current_user.id)
        if not bcrypt.check_password_hash(user.password, old_password.data):
            raise ValidationError("Password did not matched.")
        
class VerifyEmailForm(FlaskForm):
    token = StringField("Verification Token", validators=[
        DataRequired(), Length(max=6)
    ], render_kw={"placeholder": "Enter your verification token here..."})
    submit = SubmitField("Submit")
