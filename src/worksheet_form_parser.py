import flask


class WorksheetFormParser:
    eng_word = "engWord"
    pl_word = "plWord"
    reserved_keys = ["facebook_field"]

    def __init__(self):
        self.translations = []

    def parse_worksheet(self, form):
        for key, value in form.items():
            if key not in self.reserved_keys:
                self.translations.append({self.eng_word: key, self.pl_word: value})

    def get(self):
        return {"translations": self.translations}

    def get_json(self):
        return flask.jsonify(self.get())
