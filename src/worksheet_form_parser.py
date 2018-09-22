import flask


class WorksheetFormParser:
    eng_word = "engWord"
    pl_word = "plWord"
    reserved_keys = ["facebook_field", "film_title", "lesson_title"]

    def __init__(self):
        self.translations = []
        self.lessonTitle = ''
        self.filmTitle = ''

    def parse_worksheet(self, form):
        self.filmTitle = form["film_title"]
        self.lessonTitle = form["lesson_title"]
        for key, value in form.items():
            if key not in self.reserved_keys:
                self.translations.append({self.eng_word: key, self.pl_word: value})

    def get(self):
        return [{"lessonTitle": self.lessonTitle, "filmTitle": self.filmTitle, "translations": self.translations}]

    def get_json(self):
        return flask.jsonify(self.get())
