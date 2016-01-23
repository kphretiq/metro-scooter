# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import *

def exciting_app_routes(app, db, mail):

    @app.route("/")
    def index():
        lines = Line.query.all()
        return render_template("index.html", lines=lines)

    @permission_required(resource="update", action="profile")
    def things():
        return render_template("things.html")
    app.add_url_rule("/things", "things", things)
