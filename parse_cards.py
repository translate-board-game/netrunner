#!/usr/bin/python3

import os
import re
import sys
import json
from collections import OrderedDict

try:
    import yaml
    from slugify import slugify_url as slugify
except ImportError as import_error:
    print("No module 'PyYAML' and/or 'awesome-slugify' installed")
    print("Please use Python 3 with installed modules from requirements.txt")
    sys.exit()


CARDS_FILE_PATH = 'cards.json'

SET_ORDER = {
    'What Lies Ahead': 1,
    'Trace Amount': 2,
    'Cyber Exodus': 3,
    'A Study in Static': 4,
    'Humanity\'s Shadow': 5,
    'Future Proof': 6,

    'Opening Moves': 1,
    'Second Thoughts': 2,
    'Mala Tempora': 3,
    'True Colors': 4,
    'Fear and Loathing': 5,
    'Double Time': 6,

    'Upstalk': 1,
    'The Spaces Between': 2,
    'First Contact': 3,
}


class folded(str):
    pass


def represent_folded_string(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')


yaml.add_representer(folded, represent_folded_string)


def represent_ordered_dict(dumper, ordered_dict):
    value = []

    for dict_key, dict_value in ordered_dict.items():
        node_key = dumper.represent_data(dict_key)
        node_value = dumper.represent_data(dict_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, represent_ordered_dict)


def clean_breaks(text):
    return re.sub(r'([\r\n]+)', '\n', text)


def main():

    is_rewrite = 'rewrite' in sys.argv
    cards = json.load(open(CARDS_FILE_PATH))

    print("From '{}' loaded {} cards".format(CARDS_FILE_PATH, len(cards)))

    if not os.path.isdir('cards'):
        os.mkdir('cards')

    added_cards_count = 0

    for card in cards:
        cycle_number = card['cyclenumber']

        if cycle_number >= 1:  # ignore alternates and specials
            set_name = card['setname']
            set_name = '{}-{}'.format(SET_ORDER.get(set_name, ''), set_name)

            dir_name = '{:02}-{}'.format(cycle_number, slugify(set_name))
            dir_path = os.path.join('cards', dir_name)

            file_name = '{:03}-{}.yaml'.format(card['number'], slugify(card['title']))
            file_path = os.path.join(dir_path, file_name)

            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)

            # Add absent cards only
            if is_rewrite or not os.path.isfile(file_path):

                card_file = open(file_path, 'w')

                card_yaml = OrderedDict()

                card_yaml['side'] = card['side']
                card_yaml['faction'] = card['faction']
                card_yaml['type'] = card['type']
                card_yaml['uniqueness'] = card['uniqueness']

                card_yaml['obvious'] = False
                card_yaml['progress'] = 0.0

                card_yaml['title'] = card['title']
                card_yaml['title_ru'] = 'нет'

                text = clean_breaks(card['text'])
                card_yaml['text'] = folded(text)
                card_yaml['text_ru'] = folded(text)

                if 'flavor' in card:
                    flavor = clean_breaks(card['flavor'])
                    card_yaml['flavor'] = folded(flavor)
                    card_yaml['flavor_ru'] = folded(flavor)

                yaml.dump(card_yaml, card_file, default_flow_style=False, allow_unicode=True, indent=4, width=70)

                added_cards_count += 1

    print('Added {} cards'.format(added_cards_count))


if __name__ == '__main__':
    main()
