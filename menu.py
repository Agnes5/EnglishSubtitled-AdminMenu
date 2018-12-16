from WordAnalysis.analyser import analyse
from WordAnalysis.parse_subtitles import parse_subtitles
from WordAnalysis.parse_xml_to_json import parse_xml_to_json
from pathlib import Path
from Admin import admin
from WordAnalysis.utils import *

DEFAULT_PATH_TO_XML = './plwordnet-4.0-visdisc.xml'
PATH_TO_DICTIONARY = 'dictionary.json'
PATH_TO_PARSED_FILMS = './parsed_films/'
PATH_TO_DIR_WITH_RESULTS = './Admin/input/'


def menu():
    while True:
        print('0. Przetwórz xml do json')
        print('1. Przetwórz napisy z filmu')
        print('1a. Przetwórz napisy z wielu filmów')
        print('2. Przeanalizuj film')
        print('2a. Przeanalizuj wszystkie przetworzone filmy')
        print('3. Otwórz webowy panel administratora służący do edycji i wysyłania wcześniej przetworzonych lekcji')
        print('q. Wyjdź')
        print()

        choice = input('Wybór: ')

        if choice == '0':
            if Path(PATH_TO_DICTIONARY).is_file():
                create_again = input('Plik json ze słownikiem już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again.lower() == 'n':
                    continue
                elif create_again.lower() != 'y':
                    print('Nie poprawna odpowiedź')
                    continue
            path_to_xml = input('Podaj ścieżkę do pliku xml ze słowosiecią (domyślnie: {}): '
                                 .format(DEFAULT_PATH_TO_XML))

            if path_to_xml == '':
                path_to_xml = DEFAULT_PATH_TO_XML

            parse_xml_to_json(path_to_xml)

        elif choice == '1':
            path_to_subtitles = input('Podaj ścieżkę do pliku z napisami: ')
            title = input('Podaj tytuł filmu (domyślnie: nazwa pliku wejściowego): ')
            if title == '':
                title = title_from_path(path_to_subtitles)

            if Path('{}{}.csv'.format(PATH_TO_PARSED_FILMS, title)).is_file():
                create_again = input('Plik z przetworzonymi napisami już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again.lower() == 'n':
                    continue
                elif create_again.lower() != 'y':
                    print('Nie poprawna odpowiedź')
                    continue

            parse_subtitles(path_to_subtitles, title, PATH_TO_PARSED_FILMS)

        elif choice == '1a':
            path_to_subtitles = input('Podaj ścieżkę do folderu z plikami z napisami: ')
            create_again = input('Czy nadpisywać pliki wynikowe jeśli będzie taka potrzeba? [Y/n]')
            if create_again.lower() != 'n' and create_again.lower() != 'y':
                print('Nie poprawna odpowiedź')
                continue
            for file in os.listdir(path_to_subtitles):
                title = title_from_path(file)

                if Path('{}{}.csv'.format(PATH_TO_PARSED_FILMS, title)).is_file():
                    if create_again.lower() == 'n':
                        continue
                print('...trwa przetwarzanie napisów z filmu: {}'.format(title))
                parse_subtitles(path_to_subtitles + file, title, PATH_TO_PARSED_FILMS)

        elif choice == '2':
            print('Film będzie analizowany na podstawie filmów znajdujących się w folderze {}'
                  .format(PATH_TO_PARSED_FILMS))

            title = input('Podaj tytuł filmu: ')

            if Path('{}{}1.csv'.format(PATH_TO_DIR_WITH_RESULTS, title)).is_file():
                create_again = input('Plik z wynikami analizy tego filmu już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again.lower() == 'n':
                    continue
                elif create_again.lower() != 'y':
                    print('Nie poprawna odpowiedź')
                    continue

            analyse(title, PATH_TO_PARSED_FILMS, PATH_TO_DIR_WITH_RESULTS, PATH_TO_DICTIONARY)

        elif choice == '2a':
            print('Filmy będą analizowane na podstawie filmów znajdujących się w folderze {}'
                  .format(PATH_TO_PARSED_FILMS))
            create_again = input('Czy nadpisywać pliki wynikowe jeśli będzie taka potrzeba? [Y/n]')
            if create_again.lower() != 'n' and create_again.lower() != 'y':
                print('Nie poprawna odpowiedź')
                continue
            parsed_films = []
            for file in os.listdir(PATH_TO_PARSED_FILMS):
                parsed_films.append(open_file(PATH_TO_PARSED_FILMS + file).readlines())

            for file in os.listdir(PATH_TO_PARSED_FILMS):
                filename_without_extension = file.split('.')[:-1]
                extension = file.split('.')[-1:]
                filename_without_extension[len(filename_without_extension) - 1] += '1'
                filename = '.'.join(filename_without_extension + extension)
                if Path(PATH_TO_DIR_WITH_RESULTS + filename).is_file():
                    if create_again.startswith('n'):
                        continue

                analyse(file.replace('.csv', ''), PATH_TO_PARSED_FILMS, PATH_TO_DIR_WITH_RESULTS,
                        PATH_TO_DICTIONARY, parsed_films)

        elif choice == '3':
            admin.start_admin_panel()
        elif choice == 'q':
            exit(0)

        else:
            print('Nieprawidłowy wybór.')

        print()


def title_from_path(path):
    filename = path.split('/')[-1]
    title = filename.replace('.srt', '')
    return title


menu()