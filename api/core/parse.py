import re
from bs4 import Tag


def parse_a_tag(tag: Tag):
    href = tag.get('href')
    return href


def parse_onclick_attr(tag: Tag):
    onclick = tag.attrs.get('onclick')
    match = re.search('window.location=\'(.*)\'', onclick)
    
    return match.group(1) if match else None


def parse_tag(tag: Tag):
    if tag.name == 'a':
        return parse_a_tag(tag)
    if tag.attrs.get('onclick') is not None:
        return parse_onclick_attr(tag)
    
    return None