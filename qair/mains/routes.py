from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")

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

