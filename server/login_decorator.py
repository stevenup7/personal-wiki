from functools import wraps
from flask import session, request, redirect, url_for


def login_required(redirect_url):
    def decoarator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not "user" in session:
                return redirect(redirect_url)
            return f(*args, **kwargs)

        return decorated_function

    return decoarator
