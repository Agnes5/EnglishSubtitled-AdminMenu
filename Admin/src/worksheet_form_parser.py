import flask
import re


class WorksheetFormParser:
    eng_word = "engWord"
    pl_word = "plWord"
    reserved_keys = ["facebook_field", "film_title", "lesson_title", "file_name"]
    eng_word_regex = re.compile("(\d+)_eng")
    apply_suffix = "_apply"
    pl_suffix = "_pl"

    def __init__(self):
        self.translations = []
        self.lessonTitle = ''
        self.filmTitle = ''

    def parse_worksheet(self, form):
        self.filmTitle = form["film_title"]
        self.lessonTitle = form["lesson_title"]
        for key, value in form.items():
            if self.eng_word_regex.fullmatch(key):
                worksheet_index = self.eng_word_regex.fullmatch(key).group(1)
                if form.get(worksheet_index + self.apply_suffix, None) is not None:
                    self.translations.append(
                        {self.eng_word: value, self.pl_word: form.get(worksheet_index + self.pl_suffix)})

    def get(self):
        return [{"lessonTitle": self.lessonTitle, "filmTitle": self.filmTitle, "translations": self.translations}]

    def get_json(self):
        return flask.jsonify(self.get())
