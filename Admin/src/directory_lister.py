import re
from os import listdir


class DirectoryLister:
    extension = re.compile("\..*")
    underscore = re.compile("_")

    def __init__(self, directory):
        self.directory = directory

    def list_folder(self):
        files = listdir(self.directory)
        files_formatted = {self.format_filename(original): original for original in files}
        return files_formatted

    @staticmethod
    def format_filename(filename):
        formatted = DirectoryLister.extension.sub(repl="", string=filename)
        formatted = DirectoryLister.underscore.sub(repl=" ", string=formatted)
        return formatted
