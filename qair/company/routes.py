from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


company = Blueprint("company", __name__, url_prefix="/company")

@company.route("/")
@company.route("/dashboard")
@login_required
def dashboard():
    return render_template("company/dashboard.html")

@company.route("/add-planes")
@login_required
def add_planes():
    return render_template("company/add-planes.html")

@company.route("/edit-planes")
@login_required
def edit_planes():
    return render_template("company/edit-planes.html")