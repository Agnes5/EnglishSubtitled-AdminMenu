import sys
import re

import nltk
import nltk.corpus as nc
from nltk.stem.wordnet import WordNetLemmatizer


def main():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "filename.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    sentences = parse_subtitles(file)
    base_words = base_form(sentences)
    print(len(base_words))
    words = remove_stop_words(base_words)
    print(len(words))
    print(words)


def parse_subtitles(file):
    text = file.read()

    result = re.sub(r'\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '\n', text)
    result = re.sub(r'[0-9]+\n', '', result)
    result = re.sub(r'\n\n', '\n', result)
    result = re.sub(r'<[a-zA-Z/]+>', '', result)
    result = re.sub(r'\n', ' ', result)
    result = re.sub(r' +', ' ', result).lower()
    result = re.sub(r'^ ', '', result)

    result = re.sub(r'\ufeff', '', result)  # what if different coding

    result = re.sub(r'\? ', '?\n', result)
    result = re.sub(r'! ', '!\n', result)
    result = re.sub(r'\. ', '.\n', result)
    result = re.sub(r'\.\.\. ', '...\n', result)
    sentences = re.split(r'\n', result)

    return sentences


def base_form(sentences):
    result = []
    for sentence in sentences:
        result.append(nltk.pos_tag(nltk.word_tokenize(sentence)))

    words = []
    print(result)

    for sentence in result:
        for word, tag in sentence:
            if tag.startswith('N'):
                words.append((word, 'n'))
            elif tag.startswith('V'):
                words.append((word, 'v'))
            elif tag.startswith('J'):
                words.append((word, 'a'))
            elif tag.startswith('RB'):
                words.append((word, 'r'))

    lemmatizer = WordNetLemmatizer()

    base_words = set()
    for word, tag in words:
        base_words.add((lemmatizer.lemmatize(word, pos=tag), tag))
    return base_words


def remove_stop_words(words):
    all_words = []
    unique_words = set()

    all_words = all_words + [(word, tag) for word, tag in words if word not in nc.stopwords.words('english') and len(word) > 1]

    for word in all_words:
        unique_words.add(word)

    return unique_words


if __name__ == '__main__':
    main()
