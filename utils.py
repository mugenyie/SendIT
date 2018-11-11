import re

def check_valid_charaters(strg, search=re.compile(r'[^a-z0-9.]').search):
    return not bool(search(strg))