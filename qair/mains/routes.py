from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")

@mains.route("/explore")
@mains.route("/")
def explore():
    return render_template("mains/explore.html")