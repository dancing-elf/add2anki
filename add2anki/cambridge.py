"""Script to extract data for selected word from http://dictionary.cambridge.org"""
import urllib.request
from bs4 import BeautifulSoup
import htmlmin
import re

# Query template for dictionary.cambridge.org
_CAMBRIDGE_QUERY_URL = \
    'http://dictionary.cambridge.org/us/search/{src}-{dst}/direct/?q={word}'

# class of span with word translation
_TRANS_CLASS = 'trans'


def translate(word, src_lang, dst_lang):
    """fetch data from cambridge.org in convenient format"""

    url, bs = _query(word, src_lang, dst_lang)
    dictionary_form = _extract_title(bs)

    # check derivation form
    if '“' in dictionary_form:
        derived = re.search(r'“([^”]*)”', dictionary_form).group(0)
        derived = derived[1:-1]
        print('"{}" is derivation from "{}". Search it.'.format(word, derived))
        url, bs = _query(derived, src_lang, dst_lang)
        dictionary_form = _extract_title(bs)

    if not re.match(r'\A[\w]+\Z', dictionary_form):
        raise Exception("Can't parse answer for {}".format(dictionary_form))

    part_of_speech = bs.find(class_='posgram').span.text
    transcription = bs.find(class_='ipa').text

    translation_body = bs.find(class_='di-body')
    _add_formatting(translation_body)
    _cleanup_html(translation_body)
    translation = _minimize(translation_body)

    return dictionary_form, \
           '<div style="font-size:16px">' \
           '<div style="font-size:1.25em;color:#444;font-style:italic">{}</div>' \
           '<div style="color:#e84427">&frasl;{}&frasl;</div>' \
           '{}' \
           '<div style="margin-top:1.25em">' \
           '<a href="{}">See more on dictionary.cambridge.org</a>' \
           '</div></div>'.format(part_of_speech, transcription, translation, url)


def _query(word, src_lang, dst_lang):
    """ Make query for word's traslation"""
    url = _CAMBRIDGE_QUERY_URL.format(src=src_lang, dst=dst_lang, word=word)
    with urllib.request.urlopen(url) as response:
        encoding = response.headers.get_content_charset()
        html = response.read().decode(encoding)
        return url, BeautifulSoup(html, 'html.parser')


def _extract_title(bs):
    """ Extract title of page"""
    return bs.find(class_='di-title').text


def _add_formatting(html):
    """ Add styles to data. Don't using class attribute because we haven't
        special Anki card type with styles"""
    # add padding between translations
    for tag in html.findAll(class_='sense-block'):
        tag['style'] = 'padding-top:1em'
    # make translation word special
    for tag in html.findAll(class_=_TRANS_CLASS):
        tag['style'] = 'color: #0096ab'
    # we don't need extra margin
    for tag in html.findAll('p'):
        tag.name = 'div'


def _cleanup_html(html):
    """ Remove unnecessary tags and attributes"""
    for tag in html.findAll('a'):
        tag.replaceWithChildren()
    for tag in html.findAll('span'):
        if _TRANS_CLASS not in tag.attrs['class']:
            tag.replaceWithChildren()
    for tag in html.findAll():
        for attr in list(tag.attrs):
            if attr != 'style':
                del tag[attr]


def _minimize(html):
    """ Minimize html to store in csv file """
    # remove '›' because it is useless, '\n' and '\t' because they
    # can break csv file
    return htmlmin.minify(str(html)
                          .replace('›', '')
                          .replace('\n', '')
                          .replace('\t', ''))
