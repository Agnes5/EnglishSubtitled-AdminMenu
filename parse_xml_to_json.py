import lxml.etree as ET
import json
import time
from tqdm import *


def parse_xml_to_json():
    tree = ET.parse('plwordnet-4.0-visdisc.xml')
    root = tree.getroot()
    parent_map = {child: parent for parent in tree.iter() for child in parent}

    dictionary = dict()
    relation_category = ['syn_words', 'pot_odp_words', 'hiper_words', 'hipo_words']
    map_id_word = dict()

    def add_translation_to_dictionary(relation_of_translation):
        key = '{}#{}'.format(word.text, pos)
        if key in dictionary and relation_of_translation in dictionary[key]:
            dictionary[key][relation_of_translation] += [map_id_word[parent_map.get(relation).text]]
        elif key in dictionary and relation_of_translation not in dictionary[key]:
            dictionary[key][relation_of_translation] = [map_id_word[parent_map.get(relation).text]]
        else:
            tmp = dict()
            tmp[relation_of_translation] = [map_id_word[parent_map.get(relation).text]]
            dictionary[key] = tmp

    for id_word in tqdm(root.findall('SYNSET/ID')):
        words = []
        for word in parent_map.get(id_word).findall('./SYNONYM/LITERAL'):
            words.append(word.text)
        map_id_word[id_word.text] = words

    with open('map_id_word.json', 'w') as fp:
        json.dump(map_id_word, fp)

    for word in tqdm(root.findall('SYNSET/SYNONYM/LITERAL')):
        pos = parent_map.get(parent_map.get(word)).find('./POS').text[0]
        relations = parent_map.get(parent_map.get(word)).findall('./ILR/TYPE')

        for relation in relations:
            if relation.text == 'Syn_plWN-PWN':
                add_translation_to_dictionary(relation_category[0])

            elif relation.text == 'synonimia_międzyrejestrowa_plWN-PWN':
                add_translation_to_dictionary(relation_category[0])

            elif relation.text == 'międzyjęzykowa_synonimia_częściowa_plWN-PWN':
                add_translation_to_dictionary(relation_category[0])

            elif relation.text == 'pot_odp_plWN-PWN':
                add_translation_to_dictionary(relation_category[1])

            elif relation.text == 'Hiper_plWN-PWN':
                add_translation_to_dictionary(relation_category[2])

            elif relation.text == 'Hipo_plWN-PWN':
                add_translation_to_dictionary(relation_category[3])

    with open('dictionary.json', 'w') as fp:
        json.dump(dictionary, fp)


parse_xml_to_json()
