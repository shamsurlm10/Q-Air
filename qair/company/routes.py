from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


company = Blueprint("company", __name__, url_prefix="/company")

@company.route("/view-company")
@login_required
def view_company():
    return render_template("company/view-company.html")

@company.route("/change-photos")
@login_required
def change_photos():
    return render_template("company/change-photos.html")

@company.route("/add-planes")
@login_required
def add_planes():
    return render_template("company/add-planes.html")

@company.route("/edit-planes")
@login_required
def edit_planes():
    return render_template("company/edit-planes.html")

@company.route("/edit-company")
@login_required
def edit_company():
    return render_template("company/edit-company.html")

@company.route("/create-flight")
@login_required
def create_flight():
    return render_template("company/create-flight.html")

@company.route("/edit-flight")
@login_required
def edit_flight():
    return render_template("company/edit-flight.html")

@company.route("/create-route")
@login_required
def create_route():
    return render_template("company/create-route.html")