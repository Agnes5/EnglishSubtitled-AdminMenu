import sys
import os


def open_nested_file(path_to_dir, filename, mode='w'):
    create_dir(path_to_dir)
    return open_file(path_to_dir + filename, mode)


def create_dir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


def open_file(path, mode='r'):
    try:
        file = open(path, mode)
    except IOError:
        print('Nie można otworzyć pliku: {}'.format(path))
        sys.exit(0)
    return file
