
"""
personal wiki server main page

the goal of this project is to crate a quick little wiki and perhaps eventually allow it to sync up
with various services espeically a local folder and google keep notes

"""
from flask import Flask
from flask import render_template, request
import os
import glob
import markdown

DATAFOLDER = "data/"
FILEEXTENSION = ".md"

app = Flask(__name__, static_folder='../ui')

@app.route("/")
def hello_world():
    return render_template('default.html', title="personal wiki")

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



"""
REST API for page CRUD

TODO:
  move into a module
  add security


"""
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


# run the app in debug mode with autoreload turned on
app.run(host="127.0.0.1", port="5000", debug=True, use_reloader=True)
