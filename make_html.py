#!/usr/bin/python3

import os
import re
import sys
import glob
from collections import defaultdict

import yaml
from jinja2 import Template


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


expansion_number_re = re.compile('\d{2}(?:-\d)?')  # e.g. 01 02-1 03 04-1


def main():

    args = []
    for arguments in sys.argv[1:]:
        for argument in arguments.split(','):
            args.append(argument)

    no_obvious = 'no-obvious' in args
    add_neutral = 'add-neutral' in args
    expansion_numbers = filter(expansion_number_re.match, args)
    expansion_numbers = set(expansion_numbers)
    expansion_numbers = sorted(expansion_numbers)
    all_expansions = not expansion_numbers

    factions = defaultdict(list)
    for expansion_dir in os.listdir('cards'):
        if all_expansions or any(map(expansion_dir.startswith, expansion_numbers)):
            for card_file in glob.glob(os.path.join('cards', expansion_dir, '*.yaml')):
                card = yaml.load(open(card_file))

                if card['type'] == 'Identity':
                    continue
                    
                if no_obvious and card['obvious']:
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

        if add_neutral and faction not in ['Runner', 'Corp']:
            title += ' + Neutral'

        if no_obvious:
            title += ' (no obvious)'

        if expansion_numbers:
            title += ' - ' + ','.join(expansion_numbers)

        template = Template(open('template.html').read())
        output = template.render(title=title, cards=cards)

        output_file_path = 'html/{}.html'.format(title)
        output_file = open(output_file_path, 'w')
        output_file.write(output)

        print("Write '{}'".format(output_file_path))


if __name__ == '__main__':
    main()
