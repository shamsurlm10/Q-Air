from datetime import datetime
from email import message
from email.policy import default
from mimetypes import init

from flask_login import UserMixin
from itsdangerous import TimedSerializer
from itsdangerous.exc import BadTimeSignature, SignatureExpired

from qair import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
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
    profile_photo = db.Column(
        db.String, default="/image/default/ProfilePhotos/default.jpg")
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
    reservations = db.relationship("Reservation", backref="profile")
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
    country = db.Column(db.String)
    city = db.Column(db.String)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(
        self,
        street: str,
        postal_code: int,
        country: str,
        city: str,
        profile_id: int
    ) -> None:
        self.street = street
        self.postal_code = postal_code
        self.country = country
        self.city = city
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
        rating: int,
        description: str,
        profile_id: int,
        company_id: int
    ) -> None:
        self.rating = rating
        self.description = description
        self.profile_id = profile_id
        self.company_id = company_id


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    # flights = db.relationship("Flight", backref="company")
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

    def __init__(self, company_name: str, profile_id: int) -> None:
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


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey("route.id"))
    airplane_id = db.Column(db.Integer, db.ForeignKey("airplane.id"))
    reservations = db.relationship("Reservation", backref="flight")
    flight_name = db.Column(db.String, nullable=False)
    depart_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, airplane_id: int, flight_name: str, depart_time: datetime, route_id: int) -> None:
        self.airplane_id = airplane_id
        self.flight_name = flight_name
        self.depart_time = depart_time
        self.route_id = route_id
    
    def getDepartDate(self):
        return self.depart_time.strftime("%d %B, %Y, %I:%M:%S %p")
        
class FlightClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String)
    airplane_id = db.Column(db.Integer, db.ForeignKey("airplane.id"))
    reservations = db.relationship("Reservation", backref="flight_class")
    cost = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, class_name: str, airplane_id: int, cost: int) -> None:
        self.class_name = class_name
        self.airplane_id = airplane_id
        self.cost = cost

class Airplane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airplane_name = db.Column(db.String)
    airplane_model = db.Column(db.String)
    flights = db.relationship("Flight", backref="airplane")
    flight_classes = db.relationship("FlightClass", backref="airplane")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    passenger_capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, airplane_name: str, airplane_model: str, company_id: int, passerger_capacity: int):
        self.airplane_name = airplane_name
        self.airplane_model = airplane_model
        self.company_id = company_id
        self.passenger_capacity = passerger_capacity


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    flights = db.relationship("Flight", backref="route")
    origin = db.Column(db.String)
    destination = db.Column(db.String)
    distance = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, origin: str, destination: str, distance: int, duration: int, company_id: int) -> None:
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.duration = duration
        self.company_id = company_id

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))
    seat_no = db.Column(db.Integer)
    eticket_id = db.Column(db.String)
    flight_class_id = db.Column(db.Integer, db.ForeignKey("flight_class.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, profile_id: int, 
                 flight_id: int, seat_no: int, 
                 eticket_id: int, flight_class_id: int) -> None:
        self.profile_id = profile_id
        self.flight_id = flight_id
        self.seat_no = seat_no
        self.flight_class_id = flight_class_id
        self.eticket_id = eticket_id