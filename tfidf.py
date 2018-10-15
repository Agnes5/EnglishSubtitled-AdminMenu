import sys
import re
import os
import math


def analysis_words_from_film(film):
    try:
        translated_film = open('./translated_films/' + film + '_result.csv', 'r')
    except IOError:
        print('Cannot open file with translated words from {}', film)
        sys.exit(0)

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
        for film in os.listdir('./translated_films'):
            if is_film_contains_word(film, word, tag):
                count_films_with_word += 1

        tfidf_number.append(tfidf(count_word_in_film, number_of_words_in_film, count_films_with_word))

    return tfidf_number


def tf(count_word_in_film, count_all_words_in_film):
    return count_word_in_film * count_all_words_in_film


def idf(count_films_with_word):
    return math.log(count_films() / count_films_with_word)


def tfidf(count_word_in_film, count_all_words_in_films, count_films_with_word):
    return tf(count_word_in_film, count_all_words_in_films) * idf(count_films_with_word)


def count_films():
    return len(os.listdir('./translated_films'))


def is_film_contains_word(film, word, tag):
    try:
        filename = './translated_films/' + film
        translated_film = open(filename, 'r')
    except IOError:
        print('Cannot open {} file'.format(filename))
        sys.exit(0)
    translations = translated_film.readlines()
    for line in translations:
        if re.split('#', line)[0] == word and re.split('#', line)[1] == tag:
            return True
    return False