import math
import sys
import re
import os
from WordAnalysis.utils import open_file


def analysis_words_from_film(title, input_dir):
    translated_film = open_file('{}{}.csv'.format(input_dir, title))

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
        count = int(line[2])

        importance_of_word = compute_importance_of_word(word, tag, count,
                                                        number_of_words_in_film,
                                                        input_dir)

        llr_number.append(importance_of_word)

    return llr_number


def compute_importance_of_word(word, tag, count, number_of_words_in_film, input_dir):
    k11 = count

    k12 = number_of_words_in_film - k11

    k21 = 0
    k22 = 0
    for title in os.listdir(input_dir):
        k21 += count_word_in_film(title, word, tag, input_dir)
        k22 += count_all_words_in_film(title, input_dir)
    k21 = k21 - k11
    k22 = k22 - k11 - k21 - k12

    return llr_2x2(k11, k12, k21, k22)


def count_word_in_film(film, word, tag, input_dir):
    filename = input_dir + film
    try:
        translated_film = open(filename, 'r')
    except IOError:
        print('Nie można otworzyć pliku {}'.format(filename))
        sys.exit(0)
    translations = translated_film.readlines()
    for line in translations:
        if re.split('#', line)[0] == word and re.split('#', line)[1] == tag:
            return int(re.split('#', line)[3])
    return 0


def count_all_words_in_film(film, input_dir):
    with open(input_dir + film) as f:
        first_line = f.readline()
        return int(re.split('#', first_line)[1])


# k11 – number of word A in film B
# k12 – number of words (without word A) in film B
# k21 – number of word A in films (without film B)
# k22 – number of words (without word A) in films (without film B)
def llr_2x2(k11, k12, k21, k22):
    return 2 * (denorm_entropy([k11 + k12, k21 + k22]) +
                denorm_entropy([k11 + k21, k12 + k22]) -
                denorm_entropy([k11, k12, k21, k22]))


def denorm_entropy(counts):
    counts = list(counts)
    total = float(sum(counts))
    return -sum([k * math.log(k/total + (k==0)) for k in counts])
