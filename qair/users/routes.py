from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

users= Blueprint("users",__name__, url_prefix="/users")

@users.route("/login", methods=["GET","POST"])
def login_user():
    return render_template("users/login.html")

@users.route("/register", methods=["GET","POST"])
def register_user():
    return render_template("users/register.html")