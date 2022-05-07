import profile
import string
import random

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair.models import Flight, Reservation
from datetime import timedelta
from qair import db
from qair.reservations.forms import *


reservations = Blueprint("reservations", __name__, url_prefix="/reservations")


@reservations.route("/flights")
def view_all_flights():
    flights = Flight.query.all()
    return render_template('reservations/view-all-flights.html', flights=flights)


@reservations.route("/payment/<int:flight_id>", methods=["GET", "POST"])
@login_required
def payment(flight_id: int):
    flight = Flight.query.get(flight_id)
    duration = flight.route.duration
    arrival_time = (flight.depart_time + timedelta(hours=duration)
                    ).strftime("%d %B, %Y, %I:%M:%S %p")
    form = PaymentForm()
    if form.validate_on_submit():
        eticket_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        flight_class = flight.airplane.flight_classes[int(
            form.flight_class.data)]
        if (not flight_class):
            flash("Flight class id value = none", "danger")
        else:
            reservation = Reservation(
                current_user.profile.id, flight.id, int(form.seat_no.data), eticket_id, flight_class.id)
            db.session.add(reservation)
            db.session.commit()
            flash("Reservation added.", "success")
            return redirect(url_for("reservations.payment_complete"))
    return render_template('reservations/payment.html', flight=flight, arrival_time=arrival_time, form=form)


@reservations.route("/payment-complete")
@login_required
def payment_complete():
    return render_template('reservations/payment-complete.html')

@reservations.route("/view-reservation")
@login_required
def view_reservation():
    reservations = Reservation.query.filter_by(profile_id = current_user.profile.id).all()
    return render_template('reservations/view-reservation.html',reservations=reservations)
