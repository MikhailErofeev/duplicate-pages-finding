#coding: utf-8
import codecs
from types import NoneType
from bs4 import BeautifulSoup, Comment, NavigableString

__author__ = 'erofeev'


def get_main_text_from_probably_html(html_doc):
    soup = BeautifulSoup(html_doc)
    remove_staff_tags(soup)
    longer_text = ""
    if isinstance(soup.body, NoneType):
        return soup.get_text().replace("\n", " ")
    for node in soup.body.find_all(["div", "span", "td", 'tr'], recursive=True):
        if has_descendants(node):
            continue
        text = node.get_text().replace("\n", " ").strip()
        if len(text) < 100:
            continue
        text = find_best_text_area_node(soup, node).get_text()
        text = text.replace("\n", " ")
        text = " ".join(text.split())
        if len(longer_text) < len(text):
            longer_text = text
    if longer_text != "":
        return longer_text
    else:
        return soup.body.get_text().replace("\n", " ")


def find_best_text_area_node(soup, node):
    body = soup.body
    parent = node.parent
    if body == parent.parent or body == parent:
        return node
    node = parent
    return node


def has_descendants(node):
    for desc in list(node.descendants):
        if not isinstance(desc, NavigableString):
            return True
    return False


def remove_staff_tags(soup):
    [tag.extract() for tag in soup("script")]
    [tag.extract() for tag in soup("style")]
    [tag.extract() for tag in soup("br")]
    [tag.extract() for tag in soup("img")]
    [tag.extract() for tag in soup("ul")]
    [tag.parent.extract() for tag in soup("form")]
    [tag.parent.extract() for tag in soup("textarea")]
    [comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]

    remove_invalid_tags(soup)

    remove_empty_tags(soup)


def remove_invalid_tags(soup):
    invalid_tags = ['b', 'i', 'u', 'p', 'a', 'strong', 'small']
    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()


def remove_empty_tags(soup):
    containers_tags = ['div', 'td', 'span']
    any_changes = True
    while any_changes:
        any_changes = False
        for tag in containers_tags:
            for match in soup.findAll(tag):
                try:
                    if not has_descendants(match) and len(match.get_text().replace("\n", "").strip()) == 0:
                        match.decompose()
                        any_changes = True
                except:
                    pass


def get_text_from_file(file_name):
    return codecs.open(file_name, "r", "utf-8").read().encode("utf-8")