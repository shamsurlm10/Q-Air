from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


admins = Blueprint("admins", __name__, url_prefix="/admins")

@admins.route("/")
@admins.route("/dashboard")
@login_required
def dashboard():
    return render_template("admins/dashboard.html")

@admins.route("/pending-request")
@login_required
def pending_request():
    return render_template("admins/pending-request.html")

@admins.route("/view_company")
@login_required
def view_company():
    return render_template("admins/view_company.html")

@admins.route("/banned-users")
@login_required
def banned_users():
    return render_template("admins/banned-users.html")

@admins.route("/search-by-id")
@login_required
def search_by_id():
    return render_template("admins/search-by-id.html")