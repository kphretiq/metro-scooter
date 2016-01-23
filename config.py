import os
import codecs

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_DATABASE_NAME = os.environ.get("SQLALCHEMY_DATABASE_NAME")

print(SQLALCHEMY_DATABASE_URI)
print(SQLALCHEMY_DATABASE_NAME)

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"
AWS_BUCKET_NAME = "metro-scooter"

SESSION_TYPE = os.environ.get("SESSION_TYPE")

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

SIGN_UP_MESSAGE = os.environ.get("SIGN_UP_MESSAGE")
SIGN_UP_SENDER = os.environ.get("SIGN_UP_SENDER")

SITE_NAME = os.environ.get("SITE_NAME")
SITE_HOLDER = os.environ.get("SITE_HOLDER")

USER_TIMEOUT = 0

# Prepare email templates
# if you have a need for craptons of email templates, you'll want to 
# come up with a different method of handling this. 
EMAIL_TEMPLATES = {}
email_template_dir = os.path.join(BASEDIR, "email-templates")
for base, subs, filenames in os.walk(email_template_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            pth = os.path.join(base, filename)
            with codecs.open(pth, "rb", "utf-8") as f:
                EMAIL_TEMPLATES[os.path.splitext(filename)[0]] = f.read()

del os
