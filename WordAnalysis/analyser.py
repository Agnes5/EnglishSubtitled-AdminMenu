import re
import sys

import os

from WordAnalysis import translator, tfidf


NUMBER_OF_WORDS = 20

def analyse(title, input_dir, output_dir):
    result_tfidf = tfidf.analysis_words_from_film(title)

    # llr method
    # result_llr = llr.analysis_words_from_film(film)

    # todo to print result for two methods, do usuniecia pozniej
    # for a, b in zip(result_tfidf, result_llr):
    #     print('T: {}    L: {}'.format(a, b))

    try:
        file = open('{}{}.csv'.format(input_dir, title), 'r')
    except IOError:
        print('Cannot open file with translated words from {}', title)
        sys.exit(0)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    result_file = open('{}{}.csv'.format(output_dir, title), 'w')

    words = []
    index = 0
    lines = file.readlines()
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        line = re.split('#', line)
        words.append((line[0], line[1], line[3].replace('\n', ''), result_tfidf[index]))
        index += 1

    words = sorted(words, key=lambda x: x[3], reverse=True)

    translated_words = 0
    index = 0
    while translated_words < NUMBER_OF_WORDS:
        word, tag, example, _ = words[index]
        index += 1
        translations = translator.translate_word(word, tag)
        if translations:
            translations = str(translations)
            translations = translations.replace('\'', '"')
            translations = translations.replace(', ', ';')
            translations = translations.replace('[', '')
            translations = translations.replace(']', '')

            result_file.write('"{}";"{}";{}\n'.format(word, example, translations))
            translated_words += 1
