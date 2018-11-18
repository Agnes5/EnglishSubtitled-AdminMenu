import re
import nltk
import nltk.corpus as nc
from nltk.stem.wordnet import WordNetLemmatizer
from WordAnalysis.utils import *


def parse_subtitles(filename, title, result_dir):
    file = open_file(filename)
    result_file = open_nested_file(result_dir, title + '.csv')

    sentences = parse_subtitles_to_sentences(file)
    (base_form_of_words, counts_words, all_words_count,
     example_sentence_for_words) = lemmatize_sentences(sentences)
    words_to_translate = remove_stop_words(base_form_of_words)

    result_file.write('all_words#' + str(all_words_count) + '\n')
    result_file.write('word#tag#count#example\n')
    for word, tag in words_to_translate:
        result_file.write('{}#{}#{}#{}\n'
                          .format(word, tag, counts_words[(word, tag)],
                                  example_sentence_for_words[(word, tag)]))


def parse_subtitles_to_sentences(file):
    text = file.read()

    # remove lines with time intervals and numbers
    text = re.sub(r'\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '\n', text)
    text = re.sub(r'[0-9]+\n', '', text)
    text = re.sub(r'\n\n', '\n', text)

    # remove html tags
    text = re.sub(r'<[a-zA-Z0-9/]+>', '', text)
    text = re.sub(r'<[^<]*>', '', text)

    text = re.sub(r'♪', '', text)


    # remove redundant white spaces
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'^ ', '', text)

    text = re.sub(r'\ufeff', '', text)  # todo what if in file is other coding

    # split text to sentence
    text = re.sub(r'\? ', '?\n', text)
    text = re.sub(r'! ', '!\n', text)
    text = re.sub(r'\. ', '.\n', text)
    text = re.sub(r'\.\.\. ', '...\n', text)
    sentences = re.split(r'\n', text)

    sentences = [sentence[:1].lower() + sentence[1:] for sentence in sentences]

    return sentences


def lemmatize_sentences(sentences):
    all_words_count = 0
    tokenized_sentences = []
    for sentence in sentences:
        tokenized_sentences.append((nltk.pos_tag(nltk.word_tokenize(sentence)), sentence))

    base_form_of_words_with_tags = set()
    counts_words = dict()
    example_sentence_for_words = dict()

    lemmatizer = WordNetLemmatizer()


    def add_to_dict_word(word, tag):
        to_add = (lemmatizer.lemmatize(word, pos=tag), tag)
        if to_add in base_form_of_words_with_tags:
            counts_words[to_add] += 1
        else:
            base_form_of_words_with_tags.add(to_add)
            counts_words[to_add] = 1
            example_sentence_for_words[to_add] = example


    for sentence, example in tokenized_sentences:
        for word, tag in sentence:
            all_words_count += 1
            if tag.startswith('N'):
                tag = 'n'
                add_to_dict_word(word, tag)
            elif tag.startswith('V'):
                tag = 'v'
                add_to_dict_word(word, tag)
            elif tag.startswith('J'):
                tag = 'a'
                add_to_dict_word(word, tag)

    return base_form_of_words_with_tags, counts_words, all_words_count, example_sentence_for_words


def remove_stop_words(words):
    all_words = [(word, tag) for word, tag in words
                 if word not in nc.stopwords.words('english') and len(word) > 1]
    return all_words
