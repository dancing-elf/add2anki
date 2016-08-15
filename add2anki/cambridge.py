"""Script to extract data for selected word from http://dictionary.cambridge.org"""
import urllib.request
from bs4 import BeautifulSoup
import re


class CambridgeNote(object):
    """ Structured information from cambridge.org about translated word

    Attributes:
        word: dictionary form of requested word
        pos_list: possible part of speech
        transcription: transcription
        translations: list of possible translations
        url: source web page
    """

    def __init__(self, word, pos_list, transcription, translations, url):
        self._word = word
        self._pos_list = pos_list
        self._transcription = transcription
        self._translations = translations
        self._url = url

    @property
    def word(self):
        return self._word

    @property
    def pos_list(self):
        return self._pos_list

    @property
    def transcription(self):
        return self._transcription

    @property
    def translations(self):
        return self._translations

    @property
    def url(self):
        return self._url

    def to_html(self):
        return '<div style="color:#444;font-style:italic">{}</div>' \
               '<div style="color:#e84427">&frasl;{}&frasl;</div>' \
               '<div style="color: #0096ab">{}</div>' \
               '<div style="margin-top:1.25em">' \
               '<a href="{}">See more on dictionary.cambridge.org</a>' \
               '</div>' \
            .format(self._join_list(self._pos_list), self._transcription,
                    self._join_list(self._translations), self._url)

    def to_string(self):
        return 'pos: {}\ntranscription:{}\ntranslation:{}\nurl:{}'\
            .format(self._join_list(self._pos_list), self._transcription,
                    self._join_list(self._translations), self._url)

    def _join_list(self, string_list):
        return ", ".join(string_list)


# Query template for dictionary.cambridge.org
_CAMBRIDGE_QUERY_URL = \
    'http://dictionary.cambridge.org/us/search/{src}-{dst}/direct/?q={word}'


def translate(word, src_lang, dst_lang):
    """fetch data from dictionary.cambridge.org in convenient format"""
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

    pos = []
    for pos_html in bs.findAll(class_='posgram'):
        pos.append(pos_html.span.text)

    transcription = bs.find(class_='ipa').text

    all_trans = []
    for translation_html in bs.findAll(class_='trans'):
        all_trans += map(str.strip, translation_html.text.split(','))

    # remove duplicates
    uniq_trans = []
    [uniq_trans.append(item) for item in all_trans if item not in uniq_trans]

    return CambridgeNote(dictionary_form, pos, transcription, uniq_trans, url)


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