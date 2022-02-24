from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from qair.users.forms import RegisterForm
from qair import bcrypt, db
from qair.models import User

users= Blueprint("users",__name__, url_prefix="/users")

@users.route("/login", methods=["GET","POST"])
def login_user():
    return render_template("users/login.html")

@users.route("/register", methods=["GET","POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # Hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(form.email.data, hashed_password, form.full_name.data, form.passport.data)
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for("users.login_user"))
    return render_template("users/register.html", form=form)

@users.route("/", methods=["GET","POST"])
def dashboard():
    return render_template("mains/homepage.html")