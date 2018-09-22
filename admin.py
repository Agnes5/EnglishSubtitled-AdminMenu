from flask import Flask
from src.directory_lister import DirectoryLister
from src.worksheet_form_parser import WorksheetFormParser
from flask import render_template
from flask import request
import requests
from src.constants import BACKEND_ROOT, ROOT
import csv

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
    return render_template("facebookLogin.html", root=ROOT, backend_root=BACKEND_ROOT)


@app.route("/worksheet", methods=['POST'])
def show_worksheet():
    words = []
    with open("input/"+request.form["File"], "r") as lesson:
        reader = csv.reader(lesson, delimiter=';', quotechar='"')
        for row in reader:
            if len(row) >= 3:
                words.append(row)
    return render_template("worksheet.html", words=words, title=DirectoryLister.format_filename(request.form["File"]))


@app.route("/upload_lesson", methods=['POST'])
def upload_lesson():
    token = request.form["facebook_field"]
    lesson = WorksheetFormParser()
    lesson.parse_worksheet(request.form)
    print(lesson.get())
    r = requests.post(url=BACKEND_ROOT+"/lessons", json=lesson.get(), headers={'Authorization': token})
    print(str(r.status_code) + " " + str(r.content))
    if r.status_code == 200:
        return render_template("uploadSuccess.html")
    else:
        return render_template("uploadFailed.html", error_code=r.status_code, lesson=lesson.get())


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
