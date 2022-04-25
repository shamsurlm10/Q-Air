from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair import bcrypt, db
from qair.models import Flight, Profile
from qair.profiles.forms import *
from qair.profiles.utils import remove_photo, save_photos

reservations = Blueprint("reservations", __name__, url_prefix="/reservations")


@reservations.route("/flights")
def view_all_flights():
    flights = Flight.query.all()
    return render_template('reservations/view-all-flights.html', flights=flights)
