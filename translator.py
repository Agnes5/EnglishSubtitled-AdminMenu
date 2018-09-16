
def translate_word(word_to_translate, tag, root, parent_map):
    syn_words = []
    hiper_words = []
    hipo_words = []
    pot_odp_words = []

    if tag == 'a':
        tag = 'j'

    for word in root.findall('SYNSET/SYNONYM/LITERAL'):
        pos = parent_map.get(parent_map.get(word)).find('./POS').text
        if word.text == word_to_translate and pos.startswith(tag):
            relations = parent_map.get(parent_map.get(word)).findall('./ILR/TYPE')

            for relation in relations:
                if relation.text == 'Syn_plWN-PWN':
                    syn_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

                elif relation.text == 'synonimia_międzyrejestrowa_plWN-PWN':
                    syn_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

                elif relation.text == 'międzyjęzykowa_synonimia_częściowa_plWN-PWN':
                    syn_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

                elif relation.text == 'pot_odp_plWN-PWN':
                    pot_odp_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

                elif relation.text == 'Hiper_plWN-PWN':
                    hiper_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

                elif relation.text == 'Hipo_plWN-PWN':
                    hipo_words += find_literals_by_id(parent_map.get(relation).text, root, parent_map)

    if len(syn_words) != 0:
        return syn_words
    elif len(pot_odp_words) != 0:
        return pot_odp_words
    elif len(hiper_words) != 0:
        return hiper_words
    else:
        return hipo_words


def find_literals_by_id(word_id, root, parent_map):
    literals = []
    for synset in root.findall('SYNSET/ID'):
        if synset.text == word_id:
            literals += [literal.text for literal in parent_map.get(synset).findall('./SYNONYM/LITERAL')]
    return literals
