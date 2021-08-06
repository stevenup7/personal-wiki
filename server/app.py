"""
personal wiki server main page

the goal of this project is to crate a quick little wiki and perhaps eventually allow it to sync up
with various services espeically a local folder and google keep notes

"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager
from google_auth import google_auth_module, init_google_auth
from login_decorator import login_required
import os
import glob
import json
import markdown

DATAFOLDER = "data/"
FILEEXTENSION = ".md"

app = Flask(__name__, static_folder="../ui")

# TODO add this to a config file
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "jkdaslf897as87fd*(&*()&(*)&FDS@#E$R"
)

app.register_blueprint(google_auth_module, url_prefix="/google_auth")
init_google_auth(app)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
    else:
        user = None
    return render_template("home.html", user=user)


@app.route("/index")
@login_required("/")
def index():
    if "user" in session:
        user = session["user"]
    else:
        user = None

    wikifiles = []
    search_string = "{}*{}".format(DATAFOLDER, FILEEXTENSION)
    for file in glob.glob(search_string):
        wikifiles.append(file.replace(FILEEXTENSION, "").replace(DATAFOLDER, ""))

    wikifiles.sort()

    print(read_content_file("index"))
    content = markdown.markdown(read_content_file("index"))
    return render_template(
        "index.html",
        file_list=wikifiles,
        title="Index",
        index_content=content,
        user=user,
    )


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/content/<page_name>")
@login_required("/")
def content_page(page_name):
    if "user" in session:
        user = session["user"]
    else:
        user = None

    content = read_content_file(page_name)
    return render_template(
        "content-page.html",
        title=page_name,
        page_name=page_name,
        content=content,
        user=user,
    )


"""
REST API for page CRUD

TODO:
  move into a module
  add security


"""


def make_file_path(fname):
    return "{}{}{}".format(DATAFOLDER, fname, FILEEXTENSION)


def check_content_file_exists(fname):
    return os.path.exists(make_file_path(fname))


def update_or_create_content_file(fname, content):
    f = open(make_file_path(fname), "w")
    f.write(content)
    f.close()


def delete_content_file(fname):
    return True


def read_content_file(fname):
    if check_content_file_exists(fname):
        f = open(make_file_path(fname), "r")
        content = f.read()
        f.close()
        return content
    else:
        return ""


@app.route("/api/content/<page_name>", methods=["GET", "POST", "DELETE"])
@login_required("/")
def content(page_name):

    if request.method == "GET":
        print(os.getcwd())
    elif request.method == "POST":
        data = request.get_json()
        update_or_create_content_file(page_name, (data["content"]))
        print("was a post")
    return os.getcwd()


# run the app in debug mode with autoreload turned on
app.run(host="127.0.0.1", port="5000", debug=True, use_reloader=True)
