import json


def translate_word(word_to_translate, tag):
    if tag == 'a':
        tag = 'j'

    word_to_translate = '{}#{}'.format(word_to_translate, tag)
    relation_category = ['syn_words', 'pot_odp_words', 'hiper_words', 'hipo_words']

    json_file = open('dictionary.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)

    if word_to_translate in json_data:
        word_in_dictionary = json_data[word_to_translate]
        for relation in relation_category:
            if relation in word_in_dictionary:
                return word_in_dictionary[relation]
