"""
libs.strings
By default, uses `en-gb.json` file inside the `strings` top-level folder.
"""
import json

default_locale = "es-gb"
cached_strings = {}


def refresh():
    print("Refreshing...")
    global cached_strings

    cached_strings = json.loads(open('libs/en-gb.json').read())


def errmsg(name):
    return cached_strings[name]


refresh()
