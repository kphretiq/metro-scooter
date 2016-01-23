# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from App.Models import *
import flask.ext.whooshalchemy
import boto
from boto.s3.key import Key

def item_routes(app, db):
    flask.ext.whooshalchemy.whoosh_index(app, Item) 

    @app.route("/item/<string:name>")
    def item(name):
        try:
            images = None
            item = Item.query.filter(Item.name == name).first()
            brand = Brand.query.filter(Brand.id == item.brand_id).first()
        except Exception as error:
            return render_template("error.html", error=error)
        return render_template("item/index.html", item=item, brand=brand)

    @permission_required(resource="administer", action="things")
    def create():
        try:
            brands = Brand.query.all()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            try:
                item = Item(
                        brand_id = request.form["brand_id"],
                        name = request.form["name"],
                        blurb = request.form["blurb"]
                        )
                db.session.add(item)
                db.session.commit()
                brand = Brand.query.filter(Brand.id == item.brand_id).first()
            except Exception as error:
                return render_template("error.html", error=error)
            return render_template(
                    "item/index.html",
                    brand=brand,
                    item=item,
                    )

        return render_template("item/create.html", brands=brands)
    app.add_url_rule(
            "/item/create",
            "item_create",
            create,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def update(item_id):
        try:
            brands = Brand.query.all()
            item = Item.query.filter(Item.id == item_id).first()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == 'POST':
            try:
                checkboxes = ["disabled",]
                for checkbox in checkboxes:
                    if checkbox in request.form:
                        setattr(item, checkbox, 1)
                    else:
                        setattr(item, checkbox, 0)

                for key in request.form:
                    if not key in checkboxes:
                        setattr(item, key, request.form[key])
                db.session.add(item)
                db.session.commit()
                brand = Brand.query.filter(Brand.id == item.brand_id).first()
            except Exception as error:
                return render_template("error.html", error=error)
            return render_template("item/index.html", brand=brand, item=item,)

        return render_template("item/create.html", brands=brands, item=item,)
    app.add_url_rule(
            "/item/update/<int:item_id>",
            "item_update",
            update,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images_delete(item_id, image_id):
        try:
            item = Item.query.filter(Item.id == item_id).first()
            image = ItemImage.query.filter_by(id=image_id).delete()
            db.session.commit()
        except Exception as error:
            return render_template("error.html", error=error)

        return render_template("/item/images.html", item=item)
    app.add_url_rule(
            "/item/images/delete/<int:item_id>/<int:image_id>",
            "item_images_delete",
            images_delete,
            methods=["GET", "POST"],
            )

    @permission_required(resource="administer", action="things")
    def images(item_id):
        try:
            item = Item.query.filter(Item.id == item_id).first()
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

            connection = boto.s3.connect_to_region(app.config["AWS_REGION"])
            bucket = connection.get_bucket(app.config["AWS_BUCKET_NAME"])
            key = Key(bucket)
            key.key = request.form["filename"]
            try:
                key.set_contents_from_filename(path)
            except Exception as error:
                return render_template("error.html", error=error)
            uri = os.path.join(
                    "https://s3.amazonaws.com",
                    app.config["AWS_BUCKET_NAME"],
                    request.form["filename"],
                    )

            try:
                image = ItemImage(
                        uri = uri,
                        alt = request.form["alt"],
                        )
                db.session.add(image)
                db.session.commit()
                item.images.append(image)
                db.session.add(item)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)

        return render_template("/item/images.html", item=item)
    app.add_url_rule(
            "/item/images/<int:item_id>",
            "item_images",
            images,
            methods=["GET", "POST"],
            )


