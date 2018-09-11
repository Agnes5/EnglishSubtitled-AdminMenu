import re
import sys

import nltk
import nltk.corpus as nc
from nltk.stem.wordnet import WordNetLemmatizer

import translator
import xml.etree.ElementTree as ET


def main():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "TheShawshankRedemption.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    sentences = parse_subtitles(file)
    base_form_of_words = lemmatize_sentences(sentences)
    words_to_translate = remove_stop_words(base_form_of_words)

    tree = ET.parse('plwordnet-4.0-visdisc.xml')
    root = tree.getroot()
    parent_map = {c: p for p in tree.iter() for c in p}

    for word, tag in words_to_translate:
        translations = translator.translate_word(word, tag, root, parent_map)
        print('word: {}, tag: {}, translations: '.format(word, tag), end='')
        for translation in translations:
            print(translation, end=', ')
        print('')


def parse_subtitles(file):
    text = file.read()

    text = re.sub(r'\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '\n', text)
    text = re.sub(r'[0-9]+\n', '', text)
    text = re.sub(r'\n\n', '\n', text)
    text = re.sub(r'<[a-zA-Z/]+>', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r' +', ' ', text).lower()
    text = re.sub(r'^ ', '', text)

    text = re.sub(r'\ufeff', '', text)  # todo what if in file is other coding

    text = re.sub(r'\? ', '?\n', text)
    text = re.sub(r'! ', '!\n', text)
    text = re.sub(r'\. ', '.\n', text)
    text = re.sub(r'\.\.\. ', '...\n', text)
    sentences = re.split(r'\n', text)

    return sentences


def lemmatize_sentences(sentences):
    tokenized_sentences = []
    for sentence in sentences:
        tokenized_sentences.append(nltk.pos_tag(nltk.word_tokenize(sentence)))

    words_with_tags = []

    for sentence in tokenized_sentences:
        for word, tag in sentence:
            if tag.startswith('N'):
                words_with_tags.append((word, 'n'))
            elif tag.startswith('V'):
                words_with_tags.append((word, 'v'))
            elif tag.startswith('J'):
                words_with_tags.append((word, 'a'))
            # there are not adverbs in xml file
            # elif tag.startswith('RB'):
            #     words_with_tags.append((word, 'r'))

    lemmatizer = WordNetLemmatizer()

    base_form_of_words_with_tags = set()
    for word, tag in words_with_tags:
        base_form_of_words_with_tags.add((lemmatizer.lemmatize(word, pos=tag), tag))
    return base_form_of_words_with_tags


def remove_stop_words(words):
    all_words = [(word, tag) for word, tag in words if word not in nc.stopwords.words('english') and len(word) > 1]

    unique_words = set()
    for word in all_words:
        unique_words.add(word)
    return unique_words


if __name__ == '__main__':
    main()
