from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair import bcrypt, db
from qair.models import Profile
from qair.profiles.forms import *
from qair.profiles.utils import remove_photo, save_photos

profiles = Blueprint("profiles", __name__, url_prefix="/profiles")

@profiles.route("/<int:id>")
@login_required
def view_profile(id: int):
    # find the profile using the provided id
    profile = Profile.query.get(id)
    # throw error if the profile is not found
    # return the html template
    return render_template("profiles/view-profile.html", profile=profile)

@profiles.route("/change-info", methods=["GET", "POST"])
@login_required
def change_profile_info():
    form = ProfileInfoForm()
    if form.validate_on_submit():
        current_user.profile.full_name = form.full_name.data
        current_user.profile.dob = form.dob.data
        current_user.profile.passport_no = form.passport_no.data
        current_user.profile.contact_no = form.contact_no.data
        current_user.profile.address.city = form.city.data
        current_user.profile.address.country = form.country.data
        try:
            current_user.profile.address.postal_code = int(form.postal_code.data)
        except:
            raise ValueError('Postal code casting error')
        current_user.profile.address.street = form.street.data
        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("profiles.change_profile_info"))
    elif request.method == "GET":
        form.full_name.data = current_user.profile.full_name
        form.dob.data = current_user.profile.dob
        form.passport_no.data = current_user.profile.passport_no
        form.contact_no.data = current_user.profile.contact_no
        form.city.data = current_user.profile.address.city
        form.country.data = current_user.profile.address.country
        form.postal_code.data = current_user.profile.address.postal_code
        form.street.data = current_user.profile.address.street
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info", form=form)

@profiles.route("/change-photos", methods=["GET", "POST"])
@login_required
def change_photos():
    form = ChangePhoto()
    if form.validate_on_submit():
        if form.profile_photo.data:
            # deleting
            file_path = current_user.profile.profile_photo
            if not ("/image/default/ProfilePhotos/default.jpg" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.profile_photo.data, current_user.id, "profile", 250, 250)
            current_user.profile.profile_photo = "/image/uploads/profile/" + photo_file
            db.session.commit()
        if form.cover_photo.data:
            # deleting
            file_path = current_user.profile.cover_photo
            if not ("/image/default/CoverPhotos/default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.cover_photo.data, current_user.id, "cover", 1040, 260)
            current_user.profile.cover_photo = "/image/uploads/cover/" + photo_file
            db.session.commit()
    return render_template("profiles/change-photos.html", active="change-photos", form=form)

@profiles.route("/verify-email", methods=["GET", "POST"])
@login_required
def verify_email():
    form = VerifyEmailForm()
    if form.validate_on_submit():
        if current_user.is_verified:
            flash('User already verified.', 'danger')
            return redirect(url_for("profiles.verify_email"))
        if not bcrypt.check_password_hash(current_user.verified_code, form.token.data):
            flash("Token did not matched!", "danger")
        else:
            current_user.verified_code = None
            current_user.is_verified = True
            db.session.commit()
            flash("Email verified successfully.", "success")
        return redirect(url_for("profiles.verify_email"))
    return render_template("profiles/verify-email.html", active="verify-email", form=form)

@profiles.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.new_password.data).decode("utf-8")
        current_user.password = hashed_password
        db.session.commit()
        flash("Password changed successfully.", "success")
        return redirect(url_for("profiles.change_password"))
    return render_template("profiles/change-password.html", active="change-password", form=form)

@profiles.route("/remove-profile-photo")
@login_required
def remove_profile_photo():
    if not ("/image/default/ProfilePhotos/default.jpg" in current_user.profile.profile_photo):
        remove_photo(current_user.profile.profile_photo)
        current_user.profile.profile_photo = "/image/default/ProfilePhotos/default.jpg"
        db.session.commit()
        flash("Profile photo removed.", "success")
    else:
        flash("Cannot remove default profile photo.", "danger")
    return redirect(url_for("profiles.change_photos"))

@profiles.route("/settings/remove-cover-photo")
@login_required
def remove_cover_photo():
    if not ("/image/default/CoverPhotos/default.png" in current_user.profile.cover_photo):
        remove_photo(current_user.profile.cover_photo)
        current_user.profile.cover_photo = "/image/default/CoverPhotos/default.png"
        db.session.commit()
        flash("Cover photo removed.", "success")
    else:
        flash("Cannot remove default cover photo.", "danger")
    return redirect(url_for("profiles.change_photos"))

@profiles.route("/payment")
@login_required
def payment():
    return render_template("profiles/payment.html")