# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import *

def metro_routes(app, db, mail):

    @app.route("/metro/<string:brand>")
    def metro(brand):
        return render_template("/metro/%s.html"%brand)

