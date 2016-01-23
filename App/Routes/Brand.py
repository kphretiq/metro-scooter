# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from App.Models import *
import flask.ext.whooshalchemy
import boto
from boto.s3.key import Key

def brand_routes(app, db):
    flask.ext.whooshalchemy.whoosh_index(app, Brand) 

    @app.route("/brand/<string:name>")
    def brand(name):
        try:
            images = None
            brand = Brand.query.filter(Brand.name == name).first()
        except Exception as error:
            return render_template("error.html", error=error)
        return render_template("brand/index.html", brand=brand)

    @permission_required(resource="administer", action="things")
    def create():
        try:
            lines = Line.query.all()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            try:
                brand = Brand(
                        line_id = request.form["line_id"],
                        name = request.form["name"],
                        blurb = request.form["blurb"]
                        )
                db.session.add(brand)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)
            return render_template(
                    "brand/index.html",
                    brand=brand,
                    lines=lines,
                    )

        return render_template("brand/create.html", lines=lines)
    app.add_url_rule(
            "/brand/create",
            "brand_create",
            create,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def update(brand_id):
        try:
            lines = Line.query.all()
            brand = Brand.query.filter(Brand.id == brand_id).first()
            for image in brand.images:
                print(image.uri)
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            try:
                checkboxes = ["disabled",]
                for checkbox in checkboxes:
                    if checkbox in request.form:
                        setattr(brand, checkbox, 1)
                    else:
                        setattr(brand, checkbox, 0)

                for key in request.form:
                    if not key in checkboxes:
                        setattr(brand, key, request.form[key])
                db.session.add(brand)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)

        return render_template(
                "brand/create.html",
                lines=lines,
                brand=brand
                )
    app.add_url_rule(
            "/brand/update/<int:brand_id>",
            "brand_update",
            update,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images_delete(brand_id, image_id):
        try:
            brand = Brand.query.filter(Brand.id == brand_id).first()
            image = BrandImage.query.filter_by(id=image_id).delete()
            db.session.commit()
        except Exception as error:
            return render_template("error.html", error=error)

        return render_template("/brand/images.html", brand=brand)
    app.add_url_rule(
            "/brand/images/delete/<int:brand_id>/<int:image_id>",
            "brand_images_delete",
            images_delete,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images(brand_id):
        try:
            brand = Brand.query.filter(Brand.id == brand_id).first()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            path = os.path.join(
                    request.form["upload_folder"],
                    request.form["filename"],
                    )
            if not os.path.exists(path):
                error = "%s not found"%path
                return render_template("error.html", error=error)
            try:
                connection = boto.s3.connect_to_region(app.config["AWS_REGION"])
                bucket = connection.get_bucket(app.config["AWS_BUCKET_NAME"])
                key = Key(bucket)
                key.key = request.form["filename"]
                key.set_contents_from_filename(path)
            except Exception as error:
                return render_template("error.html", error=error)
            uri = os.path.join(
                    "https://s3.amazonaws.com",
                    app.config["AWS_BUCKET_NAME"],
                    request.form["filename"],
                    )

            try:
                image = BrandImage(
                        uri = uri,
                        alt = request.form["alt"],
                        )
                db.session.add(image)
                db.session.commit()
                brand.images.append(image)
                db.session.add(brand)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)

        return render_template("/brand/images.html", brand=brand)
    app.add_url_rule(
            "/brand/images/<int:brand_id>",
            "brand_images",
            images,
            methods=["GET", "POST"],
            )


