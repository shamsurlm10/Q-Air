from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (FileField, PasswordField, StringField, SubmitField,
                     IntegerField, DateTimeField)
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
    save = SubmitField("Create")
    
class CreateFlight(FlaskForm):
    flight_name = StringField("Flight Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Flight Name"})
    airplane_name = StringField("Airplane Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Name"})
    departure_time = DateTimeField("Departure Time", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Departure Time"})
    save = SubmitField("Create")
    
class EditFlight(FlaskForm):
    flight_name = StringField("Flight Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Flight Name"})
    airplane_name = StringField("Airplane Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Name"})
    departure_time = DateTimeField("Departure Time", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Departure Time"})
    update = SubmitField("Update")
    delete = SubmitField("Delete")

class CreateRoute(FlaskForm):
    origin = StringField("Origin", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Origin"})
    destination = StringField("Destination", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Destination"})
    distance = IntegerField("Distance", validators=[
        DataRequired()], render_kw={"placeholder": "Distance"})
    duration = IntegerField("Duration", validators=[
        DataRequired()], render_kw={"placeholder": "Duration"})
    save = SubmitField("Create")
    
class AddPlanes(FlaskForm):
    airplane_name = StringField("Airplane Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Name"})
    
    airplane_model = StringField("Airplane Model", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Model"})
    
    passenger_capacity = IntegerField("Passenger Capacity", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Passenger Capacity"})
    
    create = SubmitField("Create")
    
class EditPlanes(FlaskForm):
     airplane_name = StringField("Airplane Name", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Name"})
    
     airplane_model = StringField("Airplane Model", validators=[
        DataRequired(), Length(max=40, min=2)
    ], render_kw={"placeholder": "Airplane Model"})
    
     passenger_capacity = IntegerField("Passenger Capacity", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Passenger Capacity"})
    
     update = SubmitField("Update")
     delete = SubmitField("Delete")
    
