import sys
import os
import chardet


def open_nested_file(path_to_dir, filename, mode='w'):
    create_dir(path_to_dir)
    return open_file(path_to_dir + filename, mode)


def create_dir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


def open_file(path, mode='r'):
    try:
        if mode == 'r':
            encoding = check_encoding(path)

            file = open(path, mode, encoding = encoding)

        else:
            file = open(path, mode, encoding='utf-8')

    except IOError:
        print('Nie można otworzyć pliku: {}'.format(path))
        sys.exit(0)
    return file


def check_encoding(path):
    file = open(path, 'rb')
    file = file.read()
    encoding = chardet.detect(file).get('encoding')
    return encoding