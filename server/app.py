
""" ------

personal wiki server main page

the goal of this project is to crate a quick little wiki and perhaps eventually allow it to sync up
with various services espeically a local folder and google keep notes

"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint, google
from user import WikiUser
import os
import glob
import json
import markdown

# allow non https (remove this for production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_folder='../ui')
login_manager = LoginManager()
login_manager.init_app(app)

#secret keys are in a non comitted json file
with open('auth_config.json') as config_file:
    auth_config = json.load(config_file)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "jkdaslf897as87fd*(&*()&(*)&FDS@#E$R")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = auth_config["web"]["client_id"]
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = auth_config["web"]["client_secret"]
google_bp = make_google_blueprint(
    scope=['https://www.googleapis.com/auth/userinfo.profile',
           'https://www.googleapis.com/auth/userinfo.email'
    ])
oapp.register_blueprint(google_bp, url_prefix="/login")

DATAFOLDER = "data/"
FILEEXTENSION = ".md"

@login_manager.user_loader
def user_loader(user_id):
    # TODO: error handling
    u = new WikiUser()
    if session["user"]
        u.is_active = true;
        u.is_authenticated = true
        u
    else:
        try:
            resp = google.get("/oauth2/v1/userinfo")
        catch
        print (resp.json())


@app.route("/")
def loginstate():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    print (resp.json())
    return "You are {email} on Google".format(email=resp.json()["email"])

@app.route("/index")
def index():
    wikifiles = []
    search_string  = "{}*{}".format(DATAFOLDER, FILEEXTENSION)
    for file in glob.glob(search_string):
        wikifiles.append(file.replace(FILEEXTENSION, "")
                         .replace(DATAFOLDER, ""))

    wikifiles.sort()

    print (read_content_file("index"))
    content = markdown.markdown(read_content_file("index"));
    return render_template('index.html', file_list=wikifiles,
                           title="Index", index_content = content)

@app.route("/content/<page_name>")
def content_page(page_name):
    content = read_content_file(page_name)
    return render_template('content-page.html', title=page_name, page_name=page_name, content=content)

""" REST API for page CRUD """


def make_file_path(fname):
    return "{}{}{}".format(DATAFOLDER,fname,FILEEXTENSION)

def check_content_file_exists(fname):
    return os.path.exists(make_file_path(fname))

def update_or_create_content_file(fname, content):
    f = open(make_file_path(fname),"w")
    f.write(content)
    f.close()


def delete_content_file(fname):
    return True

def read_content_file(fname):
    if check_content_file_exists(fname):
        f = open(make_file_path(fname),"r")
        content = f.read()
        f.close()
        return content
    else:
        return ""

@app.route("/api/content/<page_name>", methods=["GET","POST","DELETE"])
def content(page_name):
    if request.method == "GET":
        print( os.getcwd())
    elif request.method == "POST":
        data = request.get_json()
        update_or_create_content_file(page_name, (data['content']))
        print ("was a post" )
    return os.getcwd()


# run the app in debug mode
app.run(debug=True, use_reloader=True)
