import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qair import bcrypt, db
from qair.company.forms import *
from qair.company.utils import remove_photo, save_photos
from qair.models import Airplane, Company, Flight, Review, Route

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/view-company/<int:id>")
@login_required
def view_company(id: int):
    company = Company.query.get(id)
    return render_template("company/view-company.html", company=company)


@company.route("/create-company", methods=["POST", "GET"])
@login_required
def create_company():
    form = CreateCompany()
    if form.validate_on_submit():
        if current_user.profile.company:
            flash("You have already created an account", "danger")
            return redirect(url_for('mains.homepage'))
        company = Company(form.company_name.data, current_user.profile.id)
        db.session.add(company)
        db.session.commit()
        flash(f"Company created", "success")
        return redirect(url_for("company.add_planes"))
    return render_template("company/create-company.html", form=form)


@company.route("/edit-company", methods=["POST", "GET"])
@login_required
def edit_company():
    form = ChangePhoto()
    company_id = current_user.profile.company.id
    company = Company.query.get(company_id)
    if not company:
        flash("Not found", "danger")
        return redirect(url_for('mains.homepage'))
    if form.validate_on_submit():
        company.company_name = form.company_name.data
        if form.profile_photo.data:
            # deleting
            file_path = current_user.profile.profile_photo
            if not ("/image/default/ProfilePhotos/default.jpg" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.profile_photo.data, current_user.id, "company_profile", 250, 250)
            company.profile_photo = "/image/uploads/company_profile/" + photo_file
            db.session.commit()
        if form.cover_photo.data:
            # deleting
            file_path = current_user.profile.cover_photo
            if not ("/image/default/CoverPhotos/default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.cover_photo.data, current_user.id, "company_cover", 1040, 260)
            company.cover_photo = "/image/uploads/company_cover/" + photo_file
            print(company.cover_photo)
            db.session.commit()
            print(current_user.profile.company.cover_photo)
    elif request.method == "GET":
        form.company_name.data = company.company_name
    return render_template("company/edit-company.html", form=form, company=company)


@company.route("/remove-profile-photo")
@login_required
def remove_profile_photo():
    if not ("/image/default/ProfilePhotos/default.jpg" in current_user.profile.company.profile_photo):
        remove_photo(current_user.profile.company.profile_photo)
        current_user.profile.company.profile_photo = "/image/default/ProfilePhotos/default.jpg"
        db.session.commit()
        flash("Profile photo removed.", "success")
    else:
        flash("Cannot remove default profile photo.", "danger")
    return redirect(url_for("company.edit_company"))


@company.route("/settings/remove-cover-photo")
@login_required
def remove_cover_photo():
    if not ("/image/default/CoverPhotos/default.png" in current_user.profile.company.cover_photo):
        remove_photo(current_user.profile.company.cover_photo)
        current_user.profile.company.cover_photo = "/image/default/CoverPhotos/default.png"
        db.session.commit()
        flash("Cover photo removed.", "success")
    else:
        flash("Cannot remove default cover photo.", "danger")
    return redirect(url_for("company.edit_company"))


@company.route("/create-flight", methods=["POST", "GET"])
@login_required
def create_flight():
    form = CreateFlight()
    airplanes = current_user.profile.company.airplanes
    routes = current_user.profile.company.routes
    if request.method == "POST":
        plane = request.form.get("plane-name")
        route = request.form.get("route-name")
        if not plane or not route:
            flash("Route or Plane should be selected", "danger")
        else:
            flight = Flight(int(plane), form.flight_name.data,
                            form.departure_time.data, int(route))
            db.session.add(flight)
            db.session.commit()
            flash("Flight Created", "success")
    return render_template("company/create-flight.html", form=form, airplanes=airplanes, len=len, routes=routes)


@company.route("/edit-flight/<int:id>", methods=["POST", "GET"])
@login_required
def edit_flight(id: int):
    form = EditFlight()
    flight = Flight.query.get(id)
    airplanes = current_user.profile.company.airplanes
    routes = current_user.profile.company.routes
    if request.method == "POST":
        # TODO
        pass
    plane = request.form.get("plane-name")
    route = request.form.get("route-name")
    form.flight_name.data = flight.flight_name
    form.departure_time.dara = flight.depart_time
    return render_template("company/edit-flight.html", form=form, flight=flight, airplanes=airplanes, routes=routes, len=len)


@company.route("/view-flight")
@login_required
def view_flight():
    airplanes = current_user.profile.company.airplanes
    routes = current_user.profile.company.routes
    flights = []
    for plane in airplanes:
        for flight in plane.flights:
            flights.append(flight)
    return render_template("company/view-flight.html", flights=flights, len=len)


@company.route("/add-planes", methods=["POST", "GET"])
@login_required
def add_planes():
    form = AddPlanes()
    if form.validate_on_submit():
        if not current_user.profile.company:
            flash('No company found!', 'danger')
            return redirect(url_for('company.add_planes'))
        airplane = Airplane(form.airplane_name.data,
                            form.airplane_model.data, current_user.profile.company.id,
                            form.passenger_capacity.data)
        db.session.add(airplane)
        db.session.commit()
        flash('Plane created.', 'success')
        return redirect(url_for("company.add_planes"))
    return render_template("company/add-planes.html", form=form)


@company.route("/view-planes", methods=["POST", "GET"])
@login_required
def view_planes():
    planes = Airplane.query.all()
    return render_template("company/view-planes.html", planes=planes)


@company.route("/edit-planes/<int:id>", methods=["POST", "GET"])
@login_required
def edit_planes(id: int):
    form = EditPlanes()
    plane = Airplane.query.get(id)
    if not plane:
        flash('Plane not found!', 'danger')
        return redirect(url_for('company.view_planes'))
    if form.validate_on_submit():
        plane.airplane_name = form.airplane_name.data
        plane.airplane_model = form.airplane_model.data
        plane.passenger_capacity = form.passenger_capacity.data
        db.session.commit()
        flash('Plane updated successfully.', 'success')
        return redirect(url_for('company.edit_planes', id=plane.id))
    form.airplane_name.data = plane.airplane_name
    form.airplane_model.data = plane.airplane_model
    form.passenger_capacity.data = plane.passenger_capacity
    return render_template("company/edit-planes.html", form=form)


@company.route("/create-route", methods=["POST", "GET"])
@login_required
def create_route():
    form = CreateRoute()
    if form.validate_on_submit():
        if not current_user.profile.company:
            flash('No company found!', 'danger')
            return redirect(url_for('company.create_route'))
        route = Route(form.origin.data, form.destination.data, form.distance.data,
                      form.duration.data, current_user.profile.company.id)
        db.session.add(route)
        db.session.commit()
        flash("Route Created.", "success")
        return redirect(url_for("company.edit_company"))
    return render_template("company/create-route.html", form=form)


@company.route("/review-company/<int:id>", methods=["POST"])
@login_required
def review_company(id: int):
    if current_user.profile.company and current_user.profile.company.id == id:
        flash("Your cannot review your own company!", "danger")
        return redirect(url_for("company.view_company", id=id))
    rating = request.form.get('rating')
    rating_desc = request.form.get('rating-desc')
    if not rating or not rating_desc:
        flash('Please select the rating and description.', 'danger')
        return redirect(url_for("company.view_company", id=id))
    review = Review(int(rating), rating_desc, current_user.profile.id, id)
    db.session.add(review)
    db.session.commit()
    flash("Review added successfully.", "success")
    return redirect(url_for("company.view_company", id=id))
