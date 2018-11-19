import json


RELATION_CATEGORY = ['syn_words', 'pot_odp_words', 'hiper_words', 'hipo_words']



def translate_word(word_to_translate, tag, dictionary_path):
    if tag == 'a':
        tag = 'j'

    word_to_translate = '{}#{}'.format(word_to_translate, tag)

    json_file = open(dictionary_path)
    json_str = json_file.read()
    json_data = json.loads(json_str)

    if word_to_translate in json_data:
        word_in_dictionary = json_data[word_to_translate]
        for relation in RELATION_CATEGORY:
            if relation in word_in_dictionary:
                return word_in_dictionary[relation]
