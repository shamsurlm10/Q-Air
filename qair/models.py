from datetime import datetime
from email import message

from flask_login import UserMixin
from itsdangerous import TimedSerializer
from itsdangerous.exc import BadTimeSignature, SignatureExpired

from qair import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verified_code = db.Column(db.String)
    profile = db.relationship("Profile", backref="user", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(
        self, email: str, password: str, verified_code: str
    ) -> None:
        self.email = email
        self.password = password
        self.verified_code = verified_code


    def get_joindate(self):
        return self.created_at.strftime("%B, %Y")

    def get_reset_token(self):
        # https://stackoverflow.com/questions/46486062/the-dumps-method-of-itsdangerous-throws-a-typeerror
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        return serializer.dumps(self.id)

    @staticmethod
    def verify_reset_key(id: int, token: str, max_age=1800):
        # 1800 seconds means 30 minutes
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        try:
            result = serializer.loads(token, max_age=max_age)
        except SignatureExpired:
            return {
                "is_authenticate": False,
                "message": "Token is expired! Please re-generate the token.",
            }
        except BadTimeSignature:
            return {"is_authenticate": False, "message": "Token is not valid."}
        if result != id:
            return {
                "is_authenticate": False,
                "message": "Token is not valid for this user.",
            }
        return {"is_authenticate": True, "message": "Password successfully changed."}

        

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String)
    profile_photo = db.Column(db.String, default="/image/default/ProfilePhotos/default.jpg")
    cover_photo = db.Column(
        db.String, default="/image/default/CoverPhotos/default.png"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    passport_no = db.Column(db.String(17))
    contact_no = db.Column(db.String(11))
    # notification = db.relationship("Notification", backref="profile")
    address = db.relationship("Address", backref="profile", uselist=False)
    reviews = db.relationship("Review", backref="profile")
    company = db.relationship("Company", backref="company", uselist=False)
    # flight_bookmarks = db.Column(db.ARRAY(db.Integer), default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(
        self,
        full_name: str,
        user_id: int,
    ) -> None:
        self.full_name = full_name
        self.user_id = user_id
    
    def getDateOfBirth(self):
        return self.dob.strftime("%d %B, %Y")
    
    def __str__(self) -> str:
        return f'{self.full_name} {self.user_id}'
    

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    country = db.Column(db.String)
    city = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(
        self,
        profile_id: int,
    ) -> None:
        self.profile_id = profile_id

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    rating = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(
        self,
        profile_id: int,
    ) -> None:
        self.profile_id = profile_id 
 
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    # flight = db.relationship("Flight", backref="company", uselist=False)
    # airplane = db.relationship("Airplan", backref="company", uselist=False)
    routes = db.relationship("Route", backref="company")
    airplanes = db.relationship("Airplane", backref="company")
    profile_photo = db.Column(
        db.String, default="/image/default/ProfilePhotos/default.png"
    )
    cover_photo = db.Column(
        db.String, default="/image/default/CoverPhotos/default.png"
    )
    reviews = db.relationship("Review", backref="company")
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self,company_name:str, profile_id:int)-> None:
        self.company_name = company_name
        self.profile_id = profile_id
        
    def getFoundedDate(self):
        return self.created_at.strftime("%d %B, %Y")
    
# class CompanyRating(db.Model):
#     company_id = db.Column(db.Integer, db.ForeignKey("comapany.id"))
#     profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
#     message = db.Column(db.String(250), nullable=False)
#     rating = db.Column(db.Integer(5))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
# class Notification(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(250), nullable=False) 
#     link = db.Column(db.String, nullable=False)
#     profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
#     is_readed = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
# class Flight(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
#     airplane_id = db.Column(db.Integer, db.ForeignKey("airplane.id"))
#     depart_time = db.Column(db.DateTime)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())

# class FlightClass(db.Model):
#     class_name = db.Column(db.String)
#     airplane_id = db.Column(db.Integer, db.ForeignKey("airplane.id"))
#     cost = db.Column(db.Integer(15))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
class Airplane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airplane_name = db.Column(db.String)
    airplane_model = db.Column(db.String)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    passenger_capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, airplane_name: str, airplane_model: str, company_id: int, passerger_capacity: int):
        self.airplane_name = airplane_name
        self.airplane_model = airplane_model
        self.company_id = company_id
        self.passenger_capacity = passerger_capacity
    
# class AirplaneRoute(db.Model):
#     airplane_id = db.Column(db.String)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    origin = db.Column(db.String)
    destination = db.Column(db.String)
    distance = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self,origin:str,destination:str,distance:int,duration:int, company_id:int)-> None:
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.duration = duration
        self.company_id = company_id
    
# class Reservation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
#     flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))
#     seat_no = db.Column(db.Integer(15))
#     eticket_id = db.Column(db.String)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())