from flask import Blueprint, session, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
import os
import json
import logging

"""
blueprint to handle google login

"""

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d - %H:%M:%S"
)
fh = logging.FileHandler("google_auth.log", "w")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

# allow non https (remove this for production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# TODO: dig more into this
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


google_auth_module = Blueprint(
    "google_auth_module", __name__, template_folder="../templates"
)


@google_auth_module.route("/")
def index():
    return "auth index {}".format(session["user"])


@google_auth_module.route("/login")
def check_login_state():
    if not google.authorized:
        log.info("sending to google for login")
        return redirect(url_for("google.login"))
    try:
        if "user" in session:
            log.info("you is logged in with a session")
            return redirect(url_for("home"))
        else:
            log.info("getting your details from google")
            resp = google.get("/oauth2/v1/userinfo")
            resp = resp.json()
            if "error" in resp:
                log.info("error in your auth process")
                # something went wrong try auth again
                # TODO: bad idea ?
                return redirect(url_for("google.login"))
            else:
                log.info("auth process looks good saving your email")
                session["user"] = resp["email"]
                return redirect(url_for("home"))
    except TokenExpiredError:
        log.info("expired token redirecting to google")
        return redirect(url_for("google.login"))

    return "You are {email} on Google".format(email=resp.json()["email"])


def init_google_auth(app):
    # secret keys are in a non comitted json file
    with open("auth_config.json") as config_file:
        auth_config = json.load(config_file)

    app.config["GOOGLE_OAUTH_CLIENT_ID"] = auth_config["web"]["client_id"]
    app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = auth_config["web"]["client_secret"]

    google_bp = make_google_blueprint(
        scope=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/plus.me",
        ]
    )

    app.register_blueprint(google_bp, url_prefix="/login")
