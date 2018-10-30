import re
from os import listdir, sep
from .constants import ARCHIVE_FOLDER_NAME


class DirectoryLister:
    extension = re.compile("\..*")
    underscore = re.compile("_")

    def __init__(self, directory):
        self.directory = directory

    def list_folder(self):
        files = listdir(self.directory)
        files.remove(ARCHIVE_FOLDER_NAME)
        files_formatted = {self.format_filename(original): original for original in files}

        files_archived = listdir(self.directory + sep + ARCHIVE_FOLDER_NAME)
        files_archived_formatted = {self.format_filename(original): ARCHIVE_FOLDER_NAME + sep + original
                                    for original in files_archived}
        return files_formatted, files_archived_formatted

    @staticmethod
    def format_filename(filename):
        formatted = DirectoryLister.extension.sub(repl="", string=filename)
        formatted = DirectoryLister.underscore.sub(repl=" ", string=formatted)
        return formatted