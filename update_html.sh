#!/bin/bash


# Remove all html-files
rm html/*.html


# Core Set starting decks with obvious cards
python3 make_html.py 01 add-neutral

# Core Set starting decks without obvious cards
python3 make_html.py 01 add-neutral no-obvious


# Creation and Control decks
python3 make_html.py 03 add-neutral no-obvious

# Honor and Profit decks
python3 make_html.py 05 add-neutral no-obvious


# Core Set + Genesis
python3 make_html.py 01,02 no-obvious

# Core Set + Creation and Control
python3 make_html.py 01,03 no-obvious

# Core Set + Genesis + Creation and Control
python3 make_html.py 01,02,03 no-obvious

# Core Set + Genesis + Creation and Control + Spin
python3 make_html.py 01,02,03,04 no-obvious

# Core Set + Genesis + Creation and Control + Spin + Honor and Profit
python3 make_html.py 01,02,03,04,05 no-obvious


# Remove useless files
rm "html/Neutral Runner - Core.html"
rm "html/Neutral Runner + obvious - Core.html"
rm "html/Neutral Runner - CaC.html"
rm "html/Neutral Runner - HaP.html"

rm "html/Neutral Corp - Core.html"
rm "html/Neutral Corp + obvious - Core.html"
rm "html/Neutral Corp - HaP.html"
rm "html/Neutral Corp - CaC.html"
