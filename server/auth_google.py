from flask_dance.contrib.google import make_google_blueprint, google

import os
import json

# allow non https (remove this for production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# TODO: dig more into this
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


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
