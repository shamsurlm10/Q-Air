from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


notifications = Blueprint("notifications", __name__)


@notifications.route("/notifications")
@login_required
def get_notifications():
    # notifications = Notification.query.filter_by(
    #     profile_id=current_user.profile.id).order_by(desc(Notification.created_at))[:20]
    return render_template("notifications/notifications.html")
