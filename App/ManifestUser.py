# -*- coding: utf-8 -*-
import datetime
import codecs
import uuid
from jinja2.environment import Environment
from jinja2.loaders import DictLoader
"""
Various non-route functions for creating users.
"""
def manifest_user(db, Profile, User, request, role, **kwargs): 
    """
    Shared user creation for Auth and Admin
    Create a user in User
    Create a profile in Profile
    Profile.user_id is foreign key to User.id
    Profile.user is User object
    accept
        request (object)
        role (string)
    return False on success
    return error on failure
    """
    try:
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        added = User.query.filter(User.username==username).first()

        if "email" in kwargs and kwargs["email"]:
            email = kwargs["email"]
            profile = Profile(user_id=added.id, username=username, email=email)
        else: 
            profile = Profile(user_id=added.id, username=username)
        db.session.add(profile)
        db.session.commit()

    except Exception as error:
        return error
    return False

def auth_age(TempAuth, key):
    """
    assure that the authorization key is less than a day old
    """
    temp_auth = TempAuth.query.filter(TempAuth.key==key).one()
    span = datetime.datetime.utcnow() - temp_auth.stamp
    if span.days >= 1:
        return False
    return temp_auth

def temp_auth(db, TempAuth, email):
    """
    create a temporary authorization key
    """
    key = str(uuid.uuid4())
    temp = TempAuth(key = key, email = email)
    db.session.add(temp)
    db.session.commit()
    return key

def email_html(app, template_name, **kwargs):
    """
    create email from jinja2 templates
    accepts app, template_name, kwargs
    kwargs contains variables for the template to render
    returns html template
    """
    environment = Environment()
    # use DictLoader to support inheritance!
    environment.loader = DictLoader(app.config["EMAIL_TEMPLATES"])
    template = environment.get_template(template_name)
    return template.render(obj=kwargs)
