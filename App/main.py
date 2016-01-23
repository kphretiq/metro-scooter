# -*- coding: utf-8 -*-
from flask import Flask, session
from flask.ext.session import Session
from flaskext.markdown import Markdown
from flask_mail import Mail
from App.Models import db
from App.Roles import auth_roles
from App.Routes.Line import line_routes
from App.Routes.Brand import brand_routes
from App.Routes.Item import item_routes
from App.Routes.ExcitingApp import exciting_app_routes
from App.Routes.Metro import metro_routes
from App.Routes.Scooters import scooters_routes
from App.Routes.Admin import admin_routes
from App.Routes.Auth import auth_routes
from App.API.Images import images
from App.API.Country import countries

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["APP_SECRET_KEY"]

# initialize db on app
db.init_app(app)

# add authentication roles 
auth = auth_roles(app)

# set session type as environment variable
Session(app)

# add markdown filter
Markdown(app, extensions=["nl2br", "fenced_code", "tables",])

# initialize mail
mail = Mail(app)

# lines
line_routes(app, db)
brand_routes(app, db)
item_routes(app, db)

# routes require database and mail object
exciting_app_routes(app, db, mail)
scooters_routes(app, db, mail)
metro_routes(app, db, mail)
admin_routes(app, db, mail)
auth_routes(app, db, mail)

# api
images(app)
countries(app)
