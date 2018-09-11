from flask import Flask
from src.directory_lister import DirectoryLister
from flask import render_template
from flask import request
import src.constants

app = Flask("src")


@app.route("/", methods=['GET'])
def file_select():
    directory_lister = DirectoryLister("input")
    return render_template("fileSelection.html", folder_content=directory_lister.list_folder())

@app.route("/logged", methods=['GET'])
def logged_in():
    return render_template("layout.html")

@app.route("/login", methods=['GET'])
def login():
    return render_template("facebookLogin.html", root=src.constants.ROOT, backend_root=src.constants.BACKEND_ROOT)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
