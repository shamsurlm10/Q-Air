from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair import bcrypt, db
from qair.models import Profile
from qair.profiles.forms import *

profiles = Blueprint("profiles", __name__, url_prefix="/profiles")

@profiles.route("/settings/change-info", methods=["GET", "POST"])
@login_required
def change_profile_info():
    form = ProfileInfoForm()
    if form.validate_on_submit():
        current_user.profile.full_name = form.full_name.data
        current_user.profile.dob = form.dob.data
        current_user.profile.passport_no = form.passport_no.data
        current_user.profile.contact_no = form.contact_no.data
        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("profiles.change_profile_info"))
    elif request.method == "GET":
        form.full_name.data = current_user.profile.full_name
        form.dob.data = current_user.profile.dob
        form.passport_no.data = current_user.profile.passport_no
        form.contact_no.data = current_user.profile.contact_no
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info", form=form)