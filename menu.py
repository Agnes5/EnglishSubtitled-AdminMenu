from WordAnalysis.analyser import analyse
from WordAnalysis.parse_subtitles import parse_subtitles
from WordAnalysis.parse_xml_to_json import parse_xml_to_json
from pathlib import Path


DEFAULT_PATH_TO_XML = './plwordnet-4.0-visdisc.xml'
PATH_TO_DICTIONARY = 'dictionary.json'
PATH_TO_PARSED_FILMS = './parsed_films/'
PATH_TO_DIR_WITH_RESULTS = './Admin/input/'


def menu():
    while True:
        print('0. Zparsuj xml do json')
        print('1. Zparsuj napisy z filmu')
        print('2. Przeanalizuj film')
        print('3. Zarządzaj tłumaczeniami')
        print('q. Wyjdź')
        print()

        choice = input('Wybór: ')

        if choice == '0':
            if Path(PATH_TO_DICTIONARY).is_file():
                create_again = input('Plik json ze słownikiem już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again == 'n':
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
                create_again = input('Plik z sparsowanymi napisami już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again == 'n':
                    continue

            parse_subtitles(path_to_subtitles, title, PATH_TO_PARSED_FILMS)

        elif choice == '2':
            print('Film będzie analizowany na podstawie filmów znajdujących się w folderze {}'
                  .format(PATH_TO_PARSED_FILMS))

            title = input('Podaj tytuł filmu: ')

            if Path('{}{}.csv'.format(PATH_TO_DIR_WITH_RESULTS, title)).is_file():
                create_again = input('Plik z wynikami analizy tego filmu już istnieje, '
                                     'czy na pewno chcesz nadpisać już istniejący plik? [Y/n] ')
                if create_again == 'n':
                    continue

            analyse(title, PATH_TO_PARSED_FILMS, PATH_TO_DIR_WITH_RESULTS, PATH_TO_DICTIONARY)

        elif choice == '3':
            # todo uruchamianie panelu admina
            pass

        elif choice == 'q':
            exit(0)

        else:
            print('Nieprawidłowy wybór.')

        print()


def title_from_path(path):
    filename = path.split('/')[-1]
    title = filename.split('.')[0]
    return title


menu()