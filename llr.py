import math

import sys

import re

import os


def analysis_words_from_film(film):
    try:
        translated_film = open('./translated_films/' + film + '_result.csv', 'r')
    except IOError:
        print('Cannot open file with translated words from {0}', film)
        sys.exit(0)

    llr_number = []

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
        k11 = int(line[2])

        k12 = number_of_words_in_film - k11

        k21 = 0
        k22 = 0
        for film in os.listdir('./translated_films'):
            k21 += count_word_in_film(film, word, tag)
            k22 += count_all_words_in_film(film)
        k21 = k21 - k11

        k22 = k22 - k11 - k21 - k12

        llr_number.append(llr_2x2(k11, k12, k21, k22))

    return llr_number

# k11 – number of word A in film B
# k12 – number of words (without word A) in film B
# k21 – number of word A in films (without film B)
# k22 – number of words (without word A) in films (without film B)
def llr_2x2(k11, k12, k21, k22):
    '''Special case of llr with a 2x2 table'''
    return 2 * (denormEntropy([k11+k12, k21+k22]) +
                denormEntropy([k11+k21, k12+k22]) -
                denormEntropy([k11, k12, k21, k22]))

def denormEntropy(counts):
    '''Computes the entropy of a list of counts scaled by the sum of the counts. If the inputs sum to one, this is just the normal definition of entropy'''
    counts = list(counts)
    total = float(sum(counts))
    # Note tricky way to avoid 0*log(0)
    return -sum([k * math.log(k/total + (k==0)) for k in counts])

def count_word_in_film(film, word, tag):
    try:
        filename = './translated_films/' + film
        translated_film = open(filename, 'r')
    except IOError:
        print('Cannot open {} file'.format(filename))
        sys.exit(0)
    translations = translated_film.readlines()
    for line in translations:
        if re.split('#', line)[0] == word and re.split('#', line)[1] == tag:
            return int(re.split('#', line)[3])
    return 0

def count_all_words_in_film(film):
    with open('./translated_films/' + film) as f:
        first_line = f.readline()
        return int(re.split('#', first_line)[1])
