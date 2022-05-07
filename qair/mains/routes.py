from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user

from qair.models import Route
from datetime import datetime

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")

@mains.route("/search-flight",methods=["POST"])
def search_flight():
    origin = request.form.get("from")
    destination = request.form.get("to")
    flight_class = request.form.get("class_name")
    flight_date = request.form.get("flight_date")
    route = Route.query.filter_by(origin=origin, destination=destination).first()
    route_flights = route.flights
    flights = filter(lambda flight: datetime.strptime(str(flight.depart_time).split(" ")[0], "%Y-%m-%d") == datetime.strptime(str(flight_date), "%Y-%m-%d"), route_flights)
    return render_template("mains/search-flight.html",flights=flights,len=len)
@mains.route("/explore")
def explore():
    return render_template("mains/explore.html")

@mains.route("/card-1")
def card_1():
    return render_template("mains/card-1.html")

@mains.route("/card-2")
def card_2():
    return render_template("mains/card-2.html")

@mains.route("/card-3")
def card_3():
    return render_template("mains/card-3.html")

@mains.route("/card-4")
def card_4():
    return render_template("mains/card-4.html")

@mains.route("/card-5")
def card_5():
    return render_template("mains/card-5.html")

@mains.route("/card-6")
def card_6():
    return render_template("mains/card-6.html")

