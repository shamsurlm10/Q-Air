from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

notifications = Blueprint("notifications", __name__)


@notifications.route("/notifications")
@login_required
def get_notifications():
    return render_template("notifications/notifications.html")


@notifications.route("/notification/mark-read/<int:id>")
@login_required
def mark_read(id: int):
    return redirect(url_for("notifications.get_notifications"))


@notifications.route("/notification/mark-read-and-go/<int:id>")
@login_required
def mark_read_and_go(id: int):
    return redirect(url_for("notifications.get_notifications"))


@notifications.route("/notification/mark_all")
@login_required
def mark_all():
    return redirect(url_for("notifications.get_notifications"))