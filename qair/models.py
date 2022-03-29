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
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    profile = db.relationship("Profile", backref="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(
        self, email: str, password: str, full_name: str, passport: int
    ) -> None:
        self.email = email
        self.password = password
        self.full_name = full_name
        self.passport = passport


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
    dob = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String, nullable=False)
    profile_photo = db.Column(
        db.String, default="/images/default/ProfilePhotos/default.jpg"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    passport_no = db.Column(db.String(17))
    contact_no = db.Column(db.String(11))
    # notification = db.relationship("Notification", backref="profile")
    address = db.relationship("Address", backref="profile")
    # flight_bookmarks = db.Column(db.ARRAY(db.Integer), default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Company(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_name = db.Column(db.String, nullable=False)
#     logo = db.Column(
#         db.String, default="/images/default/Logos/placeholder.png"
#     )
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
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
    

    