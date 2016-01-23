# -*- coding: utf-8 -*-
import datetime
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required, logout
from flask_mail import Message
from App.Models import Profile, User, TempAuth
from App.ManifestUser import manifest_user, auth_age, temp_auth, email_html

def auth_routes(app, db, mail):

    @app.route("/auth/signup", methods=["POST",])
    def signup():
        email = request.form["email"]
        if not email:
            error = "No email address provided."
            return render_template("error.html", error=error)

        # if no user with this email, we are good
        try:
            profile = Profile.query.filter(Profile.email==email).one()
            error = "A user already exists with this email address."
            return render_template("error.html", error=error)
        except:
            pass

        try:
            key = temp_auth(db, TempAuth, email) 
        except Exception as error:
            return render_template("error.html", error=error)

        # set as environment variable. use your own judgement.
        message = Message(
                app.config["SIGN_UP_MESSAGE"],
                sender=app.config["SIGN_UP_SENDER"],
                recipients = [email],
                )

        message.html = email_html(
                app,
                "sign-up",
                url_root = request.url_root,
                key = key,
                )

        mail.send(message)
        return render_template("auth/signup-thanks.html", email=email)

    @app.route("/auth/complete-signup/<string:key>", methods=["GET", "POST",])
    def complete_signup(key):
        if request.method == "POST":
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]

            if User.query.filter(User.username==username).first():
                error = 'User already exists.'
                return render_template("error.html", error=error)

            temp_auth = TempAuth.query.filter(TempAuth.key == key).one()
            error = manifest_user(
                    db, Profile, User, request, "user", email=temp_auth.email)
            if not error:
                return render_template("auth/login.html", username=username)
            return render_template("error.html", error=error)
        temp_auth = auth_age(TempAuth, key)
        if not temp_auth:
            stale = "Key is too old. Please send another signup email."
            return render_template("auth/login.html", stale = stale)
        return render_template("admin/create-user.html", temp_auth=temp_auth)


    @app.route("/auth/password-reset", methods=["POST",])
    def password_reset():
        email = request.form["email"]
        print(email)
        if not email:
            error = "No email address provided."
            return render_template("error.html", error=error)

        # if no user with this email, we are good
        try:
            profile = Profile.query.filter(Profile.email==email).one()
        except Exception as error:
            #error = "No user with that email address."
            return render_template("error.html", error=error)

        try:
            key = temp_auth(db, TempAuth, email) 
        except Exception as error:
            return render_template("error.html", error=error)

        # set as environment variable. use your own judgement.
        message = Message(
                app.config["SIGN_UP_MESSAGE"],
                sender=app.config["SIGN_UP_SENDER"],
                recipients = [email],
                )

        # password-reset is also name of template, in case you are me
        message.html = email_html(
                app,
                "password-reset",
                url_root = request.url_root,
                key = key,
                )

        mail.send(message)
        return render_template("auth/signup-thanks.html", email=email)

    @app.route("/auth/complete-password-reset/<string:key>", methods=[
        "GET", "POST",])
    def complete_password_reset(key):
        if request.method == "POST":
            password = request.form["password"]
            password2 = request.form["password2"]
            if not password == password2:
                error = "passwords do not match"
                return render_template("error.html", error=error)
            try:
                temp_auth = TempAuth.query.filter(TempAuth.key==key).first()
                profile = Profile.query.filter(
                        Profile.email==temp_auth.email
                        ).first()

                user = User.query.filter(User.id==profile.id).first()
                username = profile.username
                user.set_and_encrypt_password(password)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)
            return render_template("auth/login.html", username=username)

        temp_auth = auth_age(TempAuth, key)
        if not temp_auth:
            stale = "Key is too old. Please send another reset email."
            return render_template("auth/login.html", stale = stale)
        return render_template(
                "auth/password-reset.html",
                temp_auth=temp_auth,
                key=key,
                )

    @app.route("/auth/profile", methods=["GET", "POST"])
    def profile():
        """
        Update profile
        If you add a field to profile.html, the corresponding field must
        be handled in Models.py! This is a sketch, people!
        """
        try:
            profile = Profile.query.filter(
                Profile.username==session["auth_user"]["username"],
                ).first()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == "POST":
            # keep track of this, you!
            for fieldname in ["email", ]:
                if not fieldname in request.form or not request.form[fieldname]:
                    return redirect(url_for("profile"))

            for fieldname in request.form:
                setattr(profile, fieldname, request.form[fieldname])
            db.session.commit()
            return redirect(url_for("profile"))

        return render_template("auth/profile.html", profile=profile)

    @app.route("/login", methods=["GET", "POST",])
    def login():
        """
        Username and password correctly supplied and profile updated redirects
        to index.
        Username and password correctly supplied w/o updated profile redirects
        to auth/profile.
        Invalid username/password returns to login.
        """
        if request.method == "POST":
            username = request.form["username"]
            profile = Profile.query.filter(Profile.username==username).first()
            try:
                user = User.query.filter(User.username==username).one()

            except Exception as error:
                return render_template(
                        "auth/login.html",
                        error = "Incorrect user name or password.",
                        username=username)

            if user is not None:
                if not user.authenticate(request.form["password"]):
                    return render_template(
                        "auth/login.html",
                        error = "Incorrect user name or password.",
                        username=username)
                
                # make sure profile is filled out
                if not profile.updated:
                    return redirect(url_for("profile"))

                # redirect us to our "next" page in session 
                # this is not ideal, and does not work unless you set the
                # "next" value in the preceeding route!
                next_page = session.get("next")
                if next_page:
                    # don't keep "next" page around
                    session["next"] = None
                    return redirect(url_for(next_page))
                return redirect(url_for("index"))

        return render_template("auth/login.html")

    @app.route("/logout")
    def logmeout():
        logout()
        session["next"] = None
        return render_template("auth/logout.html")
