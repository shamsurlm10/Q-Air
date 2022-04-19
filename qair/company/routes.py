import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair.company.utils import remove_photo, save_photos
from qair.company.forms import *
from qair import bcrypt, db
from qair.models import Company

company = Blueprint("company", __name__, url_prefix="/company")

@company.route("/view-company")
@login_required
def view_company():
    return render_template("company/view-company.html")

@company.route("/create-company",methods=["POST","GET"])
@login_required
def create_company():
    form = CreateCompany()
    if form.validate_on_submit():
         company = Company(form.company_name.data, form.profile_photo.data, form.cover_photo.data, current_user.profile.id)
         db.session.add(company)
         db.session.commit()
         flash(f"Company created", "success")
         return redirect(url_for("company.add_planes"))
    return render_template("company/create-company.html",form=form)

@company.route("/add-planes")
@login_required
def add_planes():
    return render_template("company/add-planes.html")

@company.route("/edit-planes")
@login_required
def edit_planes():
    return render_template("company/edit-planes.html")

@company.route("/edit-company")
@login_required
def edit_company():
    pass
    # form = ChangePhoto()
    # company_id = current_user.profile.company.id
    # company = Company.query.get(company_id)
    # # if not company:
    # #     flash("Not found", "danger")
    # #     return redirect(url_for('mains.homepage'))
    # print(current_user.profile.company.id)
    # if form.validate_on_submit():
    #     company.company_name = form.company_name.data
    #     if form.profile_photo.data:
    #         # deleting
    #         file_path = current_user.profile.profile_photo
    #         if not ("/image/default/ProfilePhotos/default.jpg" in file_path):
    #             remove_photo(file_path)
    #         # saving
    #         photo_file = save_photos(
    #             form.profile_photo.data, current_user.id, "profile", 250, 250)
    #         company.profile_photo = "/image/uploads/company_profile/" + photo_file
    #         db.session.commit()
    #     if form.cover_photo.data:
    #         # deleting
    #         file_path = current_user.profile.cover_photo
    #         if not ("/image/default/CoverPhotos/default.png" in file_path):
    #             remove_photo(file_path)
    #         # saving
    #         photo_file = save_photos(
    #             form.cover_photo.data, current_user.id, "cover", 1040, 260)
    #         company.cover_photo = "/image/uploads/company_cover/" + photo_file
    #         db.session.commit()
    # elif request.method == "GET":
    #     form.company_name.data = company.company_name
    # return render_template("company/edit-company.html", form=form, company=company)

@company.route("/create-flight")
@login_required
def create_flight():
    return render_template("company/create-flight.html")

@company.route("/edit-flight")
@login_required
def edit_flight():
    return render_template("company/edit-flight.html")

@company.route("/create-route")
@login_required
def create_route():
    return render_template("company/create-route.html")