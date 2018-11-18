import re
from os import listdir, sep
from .constants import ARCHIVE_FOLDER_NAME


class DirectoryLister:
    extension = re.compile("\.[a-zA-Z0-9]+$")
    whitespace_equivalents = re.compile("[_.]")

    def __init__(self, directory, root_folder):
        self.directory = directory
        self.root_folder = root_folder

    def list_folder(self):
        files = listdir(self.root_folder + sep + self.directory)
        files_archived = dict()
        if ARCHIVE_FOLDER_NAME in files:
            files.remove(ARCHIVE_FOLDER_NAME)
            files_archived = self._list_archive_folder()
        files_formatted = {self.format_filename(original): original for original in files}

        return files_formatted, files_archived

    def _list_archive_folder(self):
        files_archived = listdir(self.root_folder + sep + self.directory + sep + ARCHIVE_FOLDER_NAME)
        return {self.format_filename(original): ARCHIVE_FOLDER_NAME + sep + original
                for original in files_archived}

    @staticmethod
    def format_filename(filename):
        formatted = DirectoryLister.extension.sub(repl="", string=filename)
        formatted = DirectoryLister.whitespace_equivalents.sub(repl=" ", string=formatted)
        return formatted
