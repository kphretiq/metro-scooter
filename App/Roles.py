# -*- coding: utf-8 -*-
from flaskext.auth import Auth, Role, Permission

def auth_roles(app):
    """
    some very basic roles.
    the "user" role can basically update their own profile
    the "admin" role can add and edit users
    the "root" profile can remove admins
    """
    auth = Auth(app, login_url_name="login")
    auth.user_timeout = app.config["USER_TIMEOUT"]

    # permission = Permission(resource, action)
    update_profile = Permission("update", "profile")
    administer_things = Permission("administer", "things")
    dangerous_things = Permission("dangerous", "things")

    roles = {
            "user": Role("user", [update_profile]),
            "admin": Role("admin", [update_profile, administer_things]),
            "root": Role("root", [update_profile, administer_things, dangerous_things]),
            }
    
    def load_role(role_name):
        return roles.get(role_name)

    auth.load_role = load_role
    return auth
