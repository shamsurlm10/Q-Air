from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair import bcrypt, db, app
from qair.models import Flight, Profile
from qair.profiles.forms import *
from qair.profiles.utils import remove_photo, save_photos
import stripe

reservations = Blueprint("reservations", __name__, url_prefix="/reservations")

@reservations.route("/flights")
def view_all_flights():
    flights = Flight.query.all()
    return render_template('reservations/view-all-flights.html', flights=flights)

@reservations.route("/payment")
def payment():
    flights = Flight.query.all()
    session = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': 'price_1KsVelHO3dppaz3nFrrX78dN',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=url_for('reservations.payment_complete', _extarnal=True)+ '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= url_for('reservations.payment', _extarnal=True),
        )
    return render_template('reservations/payment.html', flights=flights, checkout_session_id=session['id'], 
                                                        checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

@reservations.route("/payment_complete")
def payment_complete():
    return render_template('reservations/payment-complete.html')