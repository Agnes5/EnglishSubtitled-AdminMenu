from flask import Flask
from src.directory_lister import DirectoryLister
from src.worksheet_form_parser import WorksheetFormParser
from src.constants import *
from flask import render_template
from flask import request
import requests
import webbrowser
import pathlib
from os import sep, rename
import csv


app = Flask("src")


@app.route("/", methods=['GET'])
def file_select():
    directory_lister = DirectoryLister(INPUT_FOLDER_NAME)
    (folder_content, archive_content) = directory_lister.list_folder()
    return render_template("fileSelection.html", folder_content=folder_content, archive_content=archive_content)


@app.route("/logged", methods=['GET'])
def logged_in():
    return render_template("layout.html")


@app.route("/login", methods=['GET'])
def login():
    return render_template("facebookLogin.html", root=ROOT, backend_root=BACKEND_ROOT)


@app.route("/worksheet", methods=['POST'])
def show_worksheet():
    words = []
    with open("input/" + request.form["File"], "r") as lesson:
        reader = csv.reader(lesson, delimiter=';', quotechar='"')
        for row in reader:
            if len(row) >= 3:
                words.append(row)
    filename = request.form["File"]
    title = DirectoryLister.format_filename(filename)
    title = str.replace(title, ARCHIVE_FOLDER_NAME + sep, '',1)
    return render_template("worksheet.html", words=words, title=title, filename=filename)


@app.route("/upload_lesson", methods=['POST'])
def upload_lesson():
    token = request.form["facebook_field"]
    filename = request.form["file_name"]
    lesson = WorksheetFormParser()
    lesson.parse_worksheet(request.form)
    print(lesson.get())
    r = requests.post(url=BACKEND_ROOT + "/lessons", json=lesson.get(), headers={'Authorization': token}, verify=False)
    print(str(r.status_code) + " " + str(r.content))
    if r.status_code == 200:
        _archive_lesson(filename)
        return render_template("uploadSuccess.html")
    else:
        return render_template("uploadFailed.html", error_code=r.status_code, lesson=lesson.get())


def _archive_lesson(filename):
    if ARCHIVE_FOLDER_NAME + sep in filename:
        return
    path = pathlib.Path(INPUT_FOLDER_NAME + sep + ARCHIVE_FOLDER_NAME)
    path.mkdir(exist_ok=True)
    rename(INPUT_FOLDER_NAME + sep + filename, INPUT_FOLDER_NAME + sep + ARCHIVE_FOLDER_NAME + sep + filename)


def start_admin_panel():
    webbrowser.open(ROOT)
    app.run(host=ROOT_HOST_ONLY, ssl_context='adhoc')


if __name__ == '__main__':
    start_admin_panel()

