import sys
import re
import tfidf
import llr
import translator
import xml.etree.ElementTree as ET


NUMBER_OF_WORDS = 20

def main():
    film = 'TheShawshankRedemption'
    result_tfidf = tfidf.analysis_words_from_film(film)

    # llr method
    # result_llr = llr.analysis_words_from_film(film)

    # to print result for two methods
    # for a, b in zip(result_tfidf, result_llr):
    #     print('T: {}    L: {}'.format(a, b))

    try:
        file = open('./translated_films/' + film + '_result.csv', 'r')
        result_file = open('./result/' + film + '_result.csv', 'w')
    except IOError:
        print('Cannot open file with translated words from {0}', film)
        sys.exit(0)

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

    tree = ET.parse('plwordnet-4.0-visdisc.xml')
    root = tree.getroot()
    parent_map = {child: parent for parent in tree.iter() for child in parent}

    translated_words = 0
    index = 0
    while translated_words < NUMBER_OF_WORDS:
        word, tag, example, _ = words[index]
        index += 1
        translations = translator.translate_word(word, tag, root, parent_map)
        if translations:
            translations = str(translations)
            translations = translations.replace('\'', '"')
            translations = translations.replace(', ', ';')
            translations = translations.replace('[', '')
            translations = translations.replace(']', '')

            result_file.write('"{}";"{}";{}\n'.format(word, example, translations))
            translated_words += 1


if __name__ == '__main__':
    main()
