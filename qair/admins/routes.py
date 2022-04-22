from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair.models import Company, Profile, User
from sqlalchemy import desc

admins = Blueprint("admins", __name__, url_prefix="/admins")

@admins.route("/")
@admins.route("/dashboard")
@login_required
def dashboard():
    users = User.query.all()
    companies = Company.query.all()
    company_length = len(companies)
    length = len(users)
    new_user = User.query.order_by(desc(User.created_at))[:4]
    profile = Profile.query.all()
    count=0
    for i in range(length):
        if not profile[i].user.is_verified:
            count+=1
    return render_template("admins/dashboard.html",length=length, count=count, users=new_user, company_length=company_length)

@admins.route("/get-profiles-by-profile-id", methods=["POST"])
@login_required
def get_profile_by_profile_id():
    pid = request.form.get("get_by_profile_id")
    return redirect(url_for("profiles.view_profile", id=pid))


@admins.route("/get-profiles-by-user-id", methods=["POST"])
@login_required
def get_profile_by_user_id():
    uid = request.form.get("get_by_user_id")
    user = User.query.get(uid)
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))


@admins.route("/get-profiles-by-email-id", methods=["POST"])
@login_required
def get_profile_by_email_id():
    email = request.form.get("get_by_email_id")
    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))

@admins.route("/pending-request")
@login_required
def pending_request():
    return render_template("admins/pending-request.html")

@admins.route("/view_companies")
@login_required
def view_companies():
    companies = Company.query.all()
    return render_template("admins/view_companies.html", companies=companies)

@admins.route("/banned-users")
@login_required
def banned_users():
    return render_template("admins/banned-users.html")

@admins.route("/search-by-id")
@login_required
def search_by_id():
    return render_template("admins/search-by-id.html")