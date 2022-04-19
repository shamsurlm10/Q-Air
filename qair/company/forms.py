from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from qair import bcrypt
from qair.models import User
from wtforms import (DateField, PasswordField, StringField, SubmitField,
                     IntegerField)
from wtforms.validators import (URL, DataRequired, EqualTo, Length, Optional,
                                ValidationError)



class ChangePhoto(FlaskForm):
    company_name = StringField("Company Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Full Name"})
    cover_photo = FileField("Cover Photo", validators=[
                            FileAllowed(["jpg", "jpeg", "png"])])
    profile_photo = FileField("Profile Photo", validators=[
                              FileAllowed(["jpg", "jpeg", "png"])])
    save = SubmitField("Update")
    
class CreateCompany(FlaskForm):
    company_name = StringField("Company Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Company Name"})
    cover_photo = FileField("Cover Photo", validators=[
                            FileAllowed(["jpg", "jpeg", "png"])])
    profile_photo = FileField("Profile Photo", validators=[
                              FileAllowed(["jpg", "jpeg", "png"])])
    save = SubmitField("Create")