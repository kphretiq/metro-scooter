# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from App.Models import *
import flask.ext.whooshalchemy
import boto
from boto.s3.key import Key

def line_routes(app, db):
    flask.ext.whooshalchemy.whoosh_index(app, Line) 

    @app.route("/line/<string:name>")
    def line(name):
        try:
            images = None
            lines = Line.query.all()
            line = Line.query.filter(Line.name == name).first()
        except Exception as error:
            return render_template("error.html", error=error)
        return render_template("line/index.html", line=line, lines=lines,)

    @permission_required(resource="administer", action="things")
    def create():
        if request.method == 'POST':
            try:
                line = Line(
                        name = request.form["name"],
                        blurb = request.form["blurb"]
                        )
                db.session.add(line)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)
            return render_template("line/index.html", line=line)

        return render_template("line/create.html")
    app.add_url_rule(
            "/line/create",
            "line_create",
            create,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def update(line_id):
        try:
            line = Line.query.filter(Line.id == line_id).first()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            try:
                checkboxes = ["disabled",]
                for checkbox in checkboxes:
                    if checkbox in request.form:
                        setattr(line, checkbox, 1)
                    else:
                        setattr(line, checkbox, 0)

                for key in request.form:
                    if not key in checkboxes:
                        setattr(line, key, request.form[key])
                db.session.add(line)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)

        return render_template("line/create.html", line=line)
    app.add_url_rule(
            "/line/update/<int:line_id>",
            "line_update",
            update,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images_delete(line_id, image_id):
        try:
            line = Line.query.filter(Line.id == line_id).first()
            image = LineImage.query.filter_by(id=image_id).delete()
            db.session.commit()
        except Exception as error:
            return render_template("error.html", error=error)

        return render_template("/line/images.html", line=line)
    app.add_url_rule(
            "/line/images/delete/<int:line_id>/<int:image_id>",
            "line_images_delete",
            images_delete,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images(line_id):
        try:
            line = Line.query.filter(Line.id == line_id).first()
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
                print(request.form["filename"])
                print(path)
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
                image = LineImage(
                        uri = uri,
                        alt = request.form["alt"],
                        )
                db.session.add(image)
                db.session.commit()
                line.images.append(image)
                db.session.add(line)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)

        return render_template("/line/images.html", line=line)
    app.add_url_rule(
            "/line/images/<int:line_id>",
            "line_images",
            images,
            methods=["GET", "POST"],
            )


