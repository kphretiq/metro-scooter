# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import Profile, User
from App.ManifestUser import manifest_user
import flask.ext.whooshalchemy

def admin_routes(app, db, mail):
    flask.ext.whooshalchemy.whoosh_index(app, Profile) 

    @app.route("/admin/init/<string:admin_secret_key>", methods=["GET", "POST"])
    def admin_init(admin_secret_key): 

        if not admin_secret_key == app.config["ADMIN_SECRET_KEY"]:
            error = 'Bogus admin key, or key timed out.'
            return render_template("admin/error.html", error=error)

        try:
            # if we have anything in the db, we should not be here!
            if User.query.first():
                error = "Root user already created. Begone."
                return render_template("error.html", error=error)
        except Exception as error:
            try:
                db.create_all()
            except Exception as error:
               return render_template("error.html", error=error)
        if request.method == 'POST':
            username = request.form['username']
            try:
                if User.query.filter(User.username==username).first():
                    error = 'User already exists.'
                    return render_template("error.html", error=error)
            except Exception as error:
                print(error)
            error = manifest_user(db, Profile, User, request, "root")
            if not error:
                return redirect(url_for("login"))
            return render_template("error.html", error=error)

        # if we're here, we are a GET
        task = "initial database and root user set up"
        message = "database created. create a new root user."
        return render_template("admin/init.html", message=message, task=task)

    @permission_required(resource="administer", action="things")
    def admin_create_user():

        if request.method == 'POST':

            if User.query.filter(User.username==request.form["username"]).first():
                return 'User already exists.'

            if Profile.query.filter(Profile.username==request.form["username"]).first():
                return 'Profile already exists.'

            error = manifest_user(db, Profile, User, request, "user")
            if not error:
                return redirect("/admin/update-user/%s"%request.form["username"])
            return render_template("error.html", error=error)

        return render_template("admin/create-user.html")
    app.add_url_rule(
            "/admin/create-user",
            "admin_create_user",
            admin_create_user,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def update_user(username):

        try:
            profile = Profile.query.filter(Profile.username==username).first()
        except Exception as error:
            return render_template("error.html", error=error)

        # if we don't have data, throw an error
        if not profile:
            error = "no data for %s"%username
            return render_template("error.html", error=error)

        # don't be a clever-pants and change root. 
        if profile.user.role == "root":
            error = "There can be only one, and that one is the one who cannot be changed by the likes of you."
            return render_template("error.html", error=error)

        # don't edit yourself here
        if profile.user.username == session["auth_user"]["username"]:
            return redirect("/auth/profile")

        if request.method == "POST":
            for fieldname in ["role", "email",]:
                if not fieldname in request.form or not request.form[fieldname]:
                    print(fieldname)
                    return redirect(url_for("update_user"))

            # make sure no funny business going on with roles.
            if request.form["role"] == "root":
                error = "No. That would be wrong."
                return render_template("error.html", error=error)

            # update role, then profile
            if not profile.user.role == "root":
                setattr(profile.user, "role", request.form["role"])
            # everything in profile form except role goes in profile object
            # yes, this is janky.
            for fieldname in request.form:
                if not fieldname == "role":
                    setattr(profile, fieldname, request.form[fieldname])
            db.session.commit()
            return redirect("/admin/update-user/%s"%username)
        return render_template("auth/profile.html", profile=profile)
    app.add_url_rule(
            "/admin/update-user/<string:username>",
            "update_user",
            update_user,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def find_and_update_user():
        if request.method == "POST":
            search_key = request.form["search_key"]
            results = Profile.query.whoosh_search(search_key)
            return render_template("admin/find-and-update-user.html", results=results)

        return render_template("admin/find-and-update-user.html")
        
    app.add_url_rule(
            "/admin/find-and-update-user",
            "find_and_update_user",
            find_and_update_user,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def delete_user(user_id):
        profile = Profile.query.filter(Profile.id == user_id).first()
        
        if request.method == "POST":
            Profile.query.filter(Profile.id == user_id).delete()
            User.query.filter(User.id == user_id).delete()
            db.session.commit()
            return render_template("admin/find-and-update-user.html")

        return render_template(
                "admin/delete-user.html", user_id=user_id, profile=profile)
        
    app.add_url_rule(
            "/admin/delete-user/<int:user_id>",
            "delete_user",
            delete_user,
            methods=["GET", "POST"],
            )


