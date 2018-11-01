import re
from WordAnalysis import translator, tfidf, llr
from WordAnalysis.utils import *


# todo do zmiany po przeanalizowaniu
NUMBER_OF_WORDS = 20


def analyse(title, input_dir, output_dir, dictionary_path, method=1):
    if method == 1:
        result = tfidf.analysis_words_from_film(title, input_dir)
    else:
        result = llr.analysis_words_from_film(title, input_dir)

    filename = title + '.csv'

    file_with_words_from_film = open_file(input_dir + filename)

    result_file = open_nested_file(output_dir, filename)

    result_with_words = map_result_number_to_words(file_with_words_from_film, result)

    write_to_file_most_valuable_words(result_with_words, result_file, dictionary_path)


def map_result_number_to_words(file_with_words_from_film, result):
    words_with_result_number = []
    index = 0

    words_from_film = file_with_words_from_film.readlines()
    words_from_film.pop(0)
    words_from_film.pop(0)

    for word_with_information in words_from_film:
        word_with_information = re.split('#', word_with_information)
        words_with_result_number.append((word_with_information[0], word_with_information[1],
                                         word_with_information[3].replace('\n', ''), result[index]))
        index += 1

    words_with_result_number = sorted(words_with_result_number, key=lambda x: x[3], reverse=True)
    return words_with_result_number


def write_to_file_most_valuable_words(result, result_file, dictionary_path):
    translated_words = 0
    index = 0

    while translated_words < NUMBER_OF_WORDS:
        word, tag, example, _ = result[index]
        index += 1
        translations = translator.translate_word(word, tag, dictionary_path)
        if translations:
            change_format_translations(translations)

            result_file.write('"{}";"{}";{}\n'.format(word, example, translations))
            translated_words += 1


def change_format_translations(translations):
    translations = str(translations)
    translations = translations.replace('\'', '"')
    translations = translations.replace(', ', ';')
    translations = translations.replace('[', '')
    translations = translations.replace(']', '')
    return translations
