

import os
import json
from collections import OrderedDict

from slugify import slugify_url as slugify
import yaml


CARDS_FILE_PATH = 'cards.json'

SET_CODES = [
    'core'
]

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

PROPERTIES = [
    # 'number',
    # 'cyclenumber',
    # 'code',
    'title',
    'text',
    'flavor',
    # 'setname',
    # 'set_code',
    # 'faction',
    'faction_code',
    'uniqueness',
]


def represent_ordered_dict(dumper, ordered_dict):
    value = []

    for dict_key, dict_value in ordered_dict.items():
        node_key = dumper.represent_data(dict_key)
        node_value = dumper.represent_data(dict_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, represent_ordered_dict)


def main():
    cards = json.load(open(CARDS_FILE_PATH))

    print("From '{}' loaded {} cards".format(CARDS_FILE_PATH, len(cards)))

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

            # if not os.path.isfile(file_path):
            if True:
                card_file = open(file_path, 'w')
                card_yaml = OrderedDict()
                card_yaml['faction_code'] = card['faction_code']
                card_yaml['uniqueness'] = card['uniqueness']
                card_yaml['title'] = card['title']
                card_yaml['title_ru'] = 'net'
                card_yaml['text'] = card['text']
                card_yaml['text_ru'] = 'net'
                if 'flavor' in card:
                    card_yaml['flavor'] = card.get('flavor', '')
                    card_yaml['flavor_ru'] = 'net'
                yaml.dump(card_yaml, card_file, default_flow_style=False, allow_unicode=True, line_break=False)


if __name__ == '__main__':
    main()
