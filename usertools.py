from functools import wraps
from flask import g, session, request, redirect, url_for
from flask import current_app as app
from model import Organisator, Schueler

UID = 1

def is_logged_in():
    return "uid" in session

def is_organisator():
    user = get_current_user()
    return user is not None and isinstance(user, Organisator)

def is_schueler():
    user = get_current_user()
    return user is not None and isinstance(user, Schueler)
    
def get_current_user():
    if not is_logged_in():
        return None
    else:
        if "user" not in g:
            g.user = g.db.get_user(UID)
        
        return g.user
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if False: #not is_logged_in():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
