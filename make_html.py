#!/usr/bin/python3

import os
import re
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


def insert_icon_spans(text):
    return re.sub(yaml_to_html_re, yaml_to_html_replace, text)


def main():

    factions = defaultdict(list)
    for card_file in glob.glob('cards/01-core-set/*.yaml'):
        card = yaml.load(open(card_file))
        if card['type'] == 'Identity':
            continue

        text_ru = card['text_ru']
        text_ru = text_ru.replace('\n', '<br>')
        text_ru = insert_icon_spans(text_ru)
        card['text_ru'] = text_ru

        factions[card['faction']].append(card)

    if not os.path.isdir('html'):
        os.mkdir('html')

    for faction, cards in factions.items():

        cards.sort(key=lambda x: x['title'])

        template = Template(open('template.html').read())
        output = template.render(title=faction, cards=cards)

        output_file_name = 'html/{}.html'.format(faction)
        output_file = open(output_file_name, 'w')
        output_file.write(output)


if __name__ == '__main__':
    main()
