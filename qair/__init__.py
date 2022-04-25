import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import stripe

load_dotenv()

# Create and Configure the App
app = Flask(__name__)

# Secret Keys
app.secret_key = os.getenv("SECRET_KEY")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51KsVZEHO3dppaz3nfFWAJRiDzEUP8Xnwvqbq5OHb7A6jH3Rw9xDJmJPQaTrBIYBPVTmnt3sVPSTvWmnNSnyPXGNI00X77FuXoK'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51KsVZEHO3dppaz3nHc3JxcGhTISvVAJVlphKRdqnRom5wlkZxKsMnlon19VjQlJUdRCLKWSZu9004HRUb6hte4dC00x6w6xOjJ'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['UPLOAD_FOLDER'] = "static/images/uploads"
# app.config["MAIL_SERVER"] = "smtp.googlemail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
# app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

# app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")


# Database
db = SQLAlchemy(app)

# Marshmallow
# ma = Marshmallow(app)

# Migration
migrate = Migrate(app, db)

# Encryption
bcrypt = Bcrypt(app)

# Login-Manager
login_manager = LoginManager(app)

login_manager.login_view = "users.login_user"
login_manager.login_message_category = "primary"


# Mail
mail = Mail(app)


import qair.models

from qair.admins.routes import admins
# from flaskr.api.comment import comments
# from flaskr.api.post import posts
# from flaskr.api.reply import replies
from qair.reservations.routes import reservations
from qair.mains.routes import mains
from qair.company.routes import company
from qair.notifications.routes import notifications
from qair.profiles.routes import profiles
from qair.users.routes import users

# Registering blueprints
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(mains)
app.register_blueprint(admins)
app.register_blueprint(company)
app.register_blueprint(reservations)
app.register_blueprint(notifications)
# app.register_blueprint(posts)
# app.register_blueprint(comments)
# app.register_blueprint(replies)