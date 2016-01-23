# -*- coding: utf-8 -*-
import boto
from flask.ext import restful

def images(app):

    api = restful.Api(app)

    def get_upload_url(filename):
        connection = boto.s3.connect_to_region(app.config["AWS_REGION"])
        url = connection.generate_url(
                300,
                "PUT",
                app.config["AWS_BUCKET_NAME"],
                filename,
                headers = {
                    "response-content-type": "application/octet-stream",
                    "x-amz-acl": "public-read",
                    },
                )
        return {"url": url}

    class SignS3(restful.Resource):
        def get(self, filename):
            url = get_upload_url(filename)
            return url
            
    api.add_resource(SignS3, "/api/sign_s3/<string:filename>")

    #TODO I suggest you take a look at zipapottam.us.
