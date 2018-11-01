import re
import os
import math

from WordAnalysis.utils import open_file


def analysis_words_from_film(title, input_dir):
    translated_film = open_file('{}{}.csv'.format(input_dir, title))

    tfidf_number = []

    translations = translated_film.readlines()

    number_of_words_in_film = int(re.split('#', translations[0])[1])

    # remove first line with number of all words in film
    translations.pop(0)

    # remove second line with header
    translations.pop(0)

    for line in translations:
        line = re.split('#', line)
        word = line[0]
        tag = line[1]
        count_word_in_film = int(line[2])

        count_films_with_word = 0
        for title in os.listdir(input_dir):
            if is_film_contains_word(title, word, tag, input_dir):
                count_films_with_word += 1

        tfidf_number.append(tfidf(count_word_in_film, number_of_words_in_film, count_films_with_word))

    return tfidf_number


def tf(count_word_in_film, count_all_words_in_film):
    return count_word_in_film * count_all_words_in_film


def idf(count_films_with_word, input_dir):
    return math.log(count_films(input_dir) / count_films_with_word)


def tfidf(count_word_in_film, count_all_words_in_films, count_films_with_word, input_dir):
    return tf(count_word_in_film, count_all_words_in_films) * idf(count_films_with_word, input_dir)


def count_films(input_dir):
    return len(os.listdir(input_dir))


def is_film_contains_word(film, word, tag, input_dir):
    filename = input_dir + film
    translated_film = open_file(filename)

    translations = translated_film.readlines()
    for line in translations:
        if re.split('#', line)[0] == word and re.split('#', line)[1] == tag:
            return True
    return False