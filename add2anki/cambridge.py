"""Script to extract data for selected word from http://dictionary.cambridge.org"""
import urllib.request
from bs4 import BeautifulSoup
import re


class CambridgeNote(object):
    """ Structured information from cambridge.org about translated word

    Attributes:
        _word: dictionary form of requested word
        _pos_list: possible part of speech
        _transcription: list of CambridgeTranslation
        _translations: list of possible translations
        _url: source web page
    """

    class CambridgeTranslation(object):
        """ Information about one possible translation of word

        Attributes:
            _title: main "theme" of translation
            _definition: detailed explanation
            _translations: list of translations in destination language
            _example: sentence with translated word for selected topic
        """

        def __init__(self, title, definition, translations, example):
            self._title = title
            self._definition = definition
            self._translations = translations
            self._example = example

        @property
        def title(self):
            return self._title

        @property
        def definition(self):
            return self._definition

        @property
        def translations(self):
            return self._translations

        @property
        def example(self):
            return self._example

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


# Query template for dictionary.cambridge.org
_CAMBRIDGE_QUERY_URL = \
    'http://dictionary.cambridge.org/us/search/{src}-{dst}/direct/?q={word}'


def translate(word, src_lang, dst_lang):
    """fetch data from dictionary.cambridge.org in convenient format"""
    url, bs = _query(word, src_lang, dst_lang)
    dict_form = _extract_title(bs)

    # check derivation form
    if '“' in dict_form:
        derived = re.search(r'“([^”]*)”', dict_form).group(0)
        derived = derived[1:-1]
        print('"{}" is derivation from "{}". Search it.'.format(word, derived))
        url, bs = _query(derived, src_lang, dst_lang)
        dict_form = _extract_title(bs)

    if not re.match(r'\A[\w]+\Z', dict_form):
        raise Exception("Can't parse answer for {}".format(dict_form))

    pos = []
    for pos_html in bs.findAll(class_='posgram'):
        pos.append(pos_html.span.text)

    transcription = bs.find(class_='ipa').text

    translations = []
    for sense_block in bs.findAll(class_='sense-block'):
        if sense_block.find(class_='phrase-block'):
            continue

        title_block = sense_block.find(class_='sense-title')
        title = title_block.text if title_block else None

        definition = sense_block.find(class_='def').text
        trans_str = sense_block.find(class_='trans').text
        trans = list(map(str.strip, trans_str.split(',')))

        example_block = sense_block.find(class_='examp')
        example = example_block.text if example_block else None

        translations.append(CambridgeNote.CambridgeTranslation(
            title, definition, trans, example))

    return CambridgeNote(dict_form, pos, transcription, translations, url)


def to_html(note):
    """ Convert CambridgeNote to html for Anki"""
    translations_html = ''
    for trans in note.translations:
        translations_html += '<div style="margin-top:0.5em">' \
                             '<div style="font-weight: bold">{}</div>' \
                             '<div>{}</div>' \
                             '<div style="color: #0096ab">{}</div>' \
                             '<div>{}</div>' \
                             '</div>'\
            .format(trans.title, trans.definition,
                    _join_list(trans.translations), trans.example)
    return '<div style="color:#444;font-style:italic">{}</div>' \
           '<div style="color:#e84427">&frasl;{}&frasl;</div>' \
           '<div>{}</div>' \
           '<div style="margin-top:1.25em">' \
           '<a href="{}">See more on dictionary.cambridge.org</a>' \
           '</div>' \
        .format(_join_list(note.pos_list), note.transcription,
                translations_html, note.url)


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


def _join_list(string_list):
    return ", ".join(string_list)