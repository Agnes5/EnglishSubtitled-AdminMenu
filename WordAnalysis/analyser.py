import re
from WordAnalysis import translator, tfidf, llr
from WordAnalysis.utils import *
import math

NUMBER_OF_WORDS = 30
MAX_NUMBER_OF_WORDS_PER_LESSON = 10
WORD_IMPORTANCE = 90000


def analyse(title, input_dir, output_dir, dictionary_path, method=1):
    print('...trwa analiza filmu: {}'.format(title))

    if method == 1:
        result = tfidf.analysis_words_from_film(title, input_dir)
    else:
        result = llr.analysis_words_from_film(title, input_dir)

    filename = title + '.csv'

    file_with_words_from_film = open_file(input_dir + filename)

    result_with_words = map_result_number_to_words(file_with_words_from_film, result)

    write_to_file_most_valuable_words(result_with_words, title, output_dir, dictionary_path)


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


def write_to_file_most_valuable_words(result, title, output_dir, dictionary_path):
    translated_words = 0
    index = 0
    word, tag, example, value = result[index]
    parsed_result = []

    while ((value > WORD_IMPORTANCE or translated_words > NUMBER_OF_WORDS)
           and translated_words < NUMBER_OF_WORDS and index < len(result)):
        word, tag, example, value = result[index]
        index += 1
        if word[0].isupper():
            print(word)
            continue
        translations = translator.translate_word(word, tag, dictionary_path)
        if translations:
            translations = change_format_translations(translations)

            example = example[:1].upper() + example[1:]

            parsed_result.append('"{}";"{}";{}\n'.format(word, example, translations))
            translated_words += 1

    number_of_words = len(parsed_result)
    number_of_lessons = int(math.ceil(number_of_words / MAX_NUMBER_OF_WORDS_PER_LESSON))
    number_of_word_per_lesson = int(number_of_words / number_of_lessons)
    rest_of_words = number_of_words % number_of_lessons

    result_files = []
    for i in range(1, number_of_lessons + 1):
        result_files.append(open_nested_file(output_dir, '{}{}.csv'.format(title, i)))

    for lesson_number in range(number_of_lessons):
        number_of_words_for_lesson = number_of_word_per_lesson
        if rest_of_words > 0:
            number_of_words_for_lesson += 1
            rest_of_words -= 1
        for word in range(number_of_words_for_lesson):
            result_files[lesson_number].write(parsed_result.pop())


def change_format_translations(translations):
    translations = str(translations)
    translations = translations.replace('\'', '"')
    translations = translations.replace(', ', ';')
    translations = translations.replace('[', '')
    translations = translations.replace(']', '')
    return translations
