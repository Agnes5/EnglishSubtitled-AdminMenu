import re
from os import listdir


class DirectoryLister:
    def __init__(self, directory):
        self.directory = directory
        self.extension = re.compile("\..*")
        self.underscore = re.compile("_")

    def list_folder(self):
        files = listdir(self.directory)
        files_formatted = {self._format_filename(original): original for original in files}
        return files_formatted

    def _format_filename(self, filename):
        formatted = self.extension.sub(repl="", string=filename)
        formatted = self.underscore.sub(repl=" ", string=formatted)
        return formatted
