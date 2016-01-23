# -*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskext.auth.models.sa import get_user_class

db = SQLAlchemy()

# authentication User class from flask-auth
User = get_user_class(db.Model)

class Profile(db.Model):
    __tablename__ = "profile"
    __searchable__ = ["username", "email"]

    id = db.Column(db.Integer, primary_key = True)
    # yes, this is redundant. Live with it.
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(254))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="profile")

class TempAuth(db.Model):
    __tablename__ = "temp_auth"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(254))
    key = db.Column(db.String(254))
    stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Line(db.Model):
    __tablename__ = "line"
    __searchable__ = ["name"]
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    blurb = db.Column(db.Text)
    image_id = db.Column(db.Integer)
    disabled = db.Column(db.Boolean, default=False)
    brands = db.relationship("Brand", backref="line", lazy="dynamic")
    images = db.relationship("LineImage", backref="line", lazy="dynamic")

class LineImage(db.Model):
    __tablename__ = "line_image"
    id = db.Column(db.Integer, primary_key = True)
    uri = db.Column(db.String(256), unique=True, nullable=False)
    alt = db.Column(db.String(64), unique=True, nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey("line.id"))

class Brand(db.Model):
    __tablename__ = "brand"
    __searchable__ = ["name"]
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    blurb = db.Column(db.Text)
    disabled = db.Column(db.Boolean, default=False)
    line_id = db.Column(db.Integer, db.ForeignKey("line.id"))
    items = db.relationship("Item", backref="brand", lazy="dynamic")
    images = db.relationship("BrandImage", backref="brand", lazy="dynamic")

class BrandImage(db.Model):
    __tablename__ = "brand_image"
    id = db.Column(db.Integer, primary_key = True)
    uri = db.Column(db.String(256), unique=True, nullable=False)
    alt = db.Column(db.String(64), unique=True, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"))

class Item(db.Model):
    __tablename__ = "item"
    __searchable__ = ["name"]
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    blurb = db.Column(db.Text)
    disabled = db.Column(db.Boolean, default=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"))
    images = db.relationship("ItemImage", backref="item", lazy="dynamic")

class ItemImage(db.Model):
    __tablename__ = "item_image"
    id = db.Column(db.Integer, primary_key = True)
    uri = db.Column(db.String(256), unique=True, nullable=False)
    alt = db.Column(db.String(64), unique=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
