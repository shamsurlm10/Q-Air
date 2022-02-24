from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from qair.users.forms import RegisterForm, LoginForm
from qair import bcrypt, db
from qair.models import User
from flask_login import login_user as login_user_function, login_required, logout_user as logout_user_function, current_user

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/login", methods=["GET", "POST"])
def login_user():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Fetching the user
        fetched_user = User.query.filter_by(email=form.email.data).first()
        # Checking the email and password
        if fetched_user and bcrypt.check_password_hash(fetched_user.password, form.password.data):
            login_user_function(fetched_user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            response = redirect(next_page) if next_page else redirect(
                url_for('users.dashboard'))
            flash("Login Successfull.", "success")
            return response
        else:
            flash("Login Failed! Please Check Email and Password.", "danger")
    return render_template("users/login.html", form=form)


@users.route("/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(form.email.data, hashed_password,
                    form.full_name.data, form.passport.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {user.full_name}", "success")
        return redirect(url_for("users.login_user"))
    return render_template("users/register.html", form=form)


@users.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("mains/homepage.html")


@users.route("/logout")
@login_required
def logout_user():
    logout_user_function()
    return redirect(url_for("users.login_user"))
