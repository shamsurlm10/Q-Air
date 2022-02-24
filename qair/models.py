from datetime import datetime

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
    passport = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
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