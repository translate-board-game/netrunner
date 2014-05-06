#!/usr/bin/python3

import os
import re
import sys
import glob
from collections import defaultdict

import yaml
from jinja2 import Template


SET_CODES = {
    '01': 'Core',

    '02': 'Genesis',
    '02-1': 'WLA',
    '02-2': 'TA',
    '02-3': 'CE',
    '02-4': 'SiS',
    '02-5': 'HS',
    '02-6': 'FP',

    '03': 'CaC',

    '04': 'Spin',
    '04-1': 'OM',
    '04-2': 'ST',
    '04-3': 'MT',
    '04-4': 'TC',
    '04-5': 'FaL',
    '04-6': 'DT',

    '05': 'HaP',
}


HTML_CLASS_SUFFIXES = {
    'Link': 'link',
    'Click': 'click',
    'Trash': 'trash',
    'Credits': 'credit',
    'Subroutine': 'subroutine',
    'Memory Unit': 'mu',
    'Recurring Credits': 'recurring-credit',
}

yaml_to_html = {}
for keyword, class_suffix in HTML_CLASS_SUFFIXES.items():
    yaml_to_html['[{}]'.format(keyword)] = '<span class="icon icon-{}"></span>'.format(class_suffix)

yaml_tags = map(re.escape, yaml_to_html.keys())
yaml_tags = '|'.join(yaml_tags)
yaml_to_html_re = re.compile('({})'.format(yaml_tags))
yaml_to_html_replace = lambda x: yaml_to_html[x.group(1)]


def convert_to_html(text):
    text = text.replace('\n', '<br>')
    text = re.sub(yaml_to_html_re, yaml_to_html_replace, text)
    return text


set_number_re = re.compile('\d{2}(?:-\d)?')  # e.g. 01 02-1 03 04-1


def main():

    args = []
    for arguments in sys.argv[1:]:
        for argument in arguments.split(','):
            args.append(argument)

    remove_obvious = 'no-obvious' in args
    add_neutral = 'add-neutral' in args
    set_numbers = filter(set_number_re.match, args)
    set_numbers = set(set_numbers)
    set_numbers = sorted(set_numbers)
    all_sets = not set_numbers

    factions = defaultdict(list)
    for set_dir in os.listdir('cards'):
        if all_sets or any(map(set_dir.startswith, set_numbers)):
            for card_file in glob.glob(os.path.join('cards', set_dir, '*.yaml')):
                card = yaml.load(open(card_file))

                if card['type'] == 'Identity':
                    continue

                if remove_obvious and card['obvious']:
                    continue

                card['text_ru'] = convert_to_html(card['text_ru'])

                faction_name = card['faction'] if card['faction'] != 'Neutral' else card['side']
                factions[faction_name].append(card)

    if add_neutral:
        for faction, cards in factions.items():
            if faction not in ['Runner', 'Corp']:
                cards.extend(factions[cards[0]['side']])

    if not os.path.isdir('html'):
        os.mkdir('html')

    for faction, cards in factions.items():

        cards.sort(key=lambda x: x['title'])

        title = faction

        if title in ['Runner', 'Corp']:
            title = 'Neutral ' + title

        if add_neutral and faction not in ['Runner', 'Corp']:
            title += ' + Neutral'

        if not remove_obvious:
            title += ' + obvious'

        if set_numbers:
            set_codes = list(map(SET_CODES.__getitem__, set_numbers))
            if not add_neutral:
                if 'CaC' in set_codes and faction not in ['Haas-Bioroid', 'Shaper', 'Runner', 'Corp']:
                    set_codes.remove('CaC')
                if 'HaP' in set_codes and faction not in ['Jinteki', 'Criminal', 'Runner', 'Corp']:
                    set_codes.remove('HaP')
            title += ' - ' + ', '.join(set_codes)

        template = Template(open('template.html').read())
        output = template.render(title=title, cards=cards)

        output_file_path = 'html/{}.html'.format(title)
        output_file = open(output_file_path, 'w')
        output_file.write(output)

        print("Write '{}'".format(output_file_path))


if __name__ == '__main__':
    main()
