"""Script to extract data for selected word from http://dictionary.cambridge.org"""
import re
import urllib.request

import colorama
from bs4 import BeautifulSoup


class CambridgeNote(object):
    """ Structured information from cambridge.org about translated word

    Attributes:
        _word: dictionary form of requested word
        _pos_list: possible part of speech
        _pronunciation: pronunciation of word
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

    def __init__(self, word, pos_list, pronunciation,
                 transcription, translations, url):
        self._word = word
        self._pos_list = pos_list
        self._pronunciation = pronunciation
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
    def pronunciation(self):
        return self._pronunciation

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

    url, bs, dict_form = _fetch_data(word, src_lang, dst_lang)

    pos_list = []
    for pos_html in bs.find_all(class_='posgram'):
        pos_list.append(pos_html.span.text)

    play_button = bs.select_one('.audio_play_button.us')
    pronunciation = play_button.attrs['data-src-ogg']

    transcription = bs.find(class_='ipa').text

    trans_list = []
    for sense_block in bs.find_all(class_='sense-block'):
        if sense_block.find(class_='phrase-block'):
            continue

        title_block = sense_block.find(class_='sense-title')
        title = title_block.text if title_block else None

        definition = sense_block.find(class_='def').text
        trans_str = sense_block.find(class_='trans').text
        trans = list(map(str.strip, trans_str.split(',')))

        example_block = sense_block.find(class_='examp')
        example = example_block.text.strip() if example_block else None

        trans_list.append(
            CambridgeNote.CambridgeTranslation(
                title, definition, trans, example))

    return CambridgeNote(dict_form, pos_list, pronunciation,
                         transcription, trans_list, url)


def to_html(note):
    """Convert CambridgeNote to html for Anki"""
    translations_html = ''
    for trans in note.translations:
        translations_html += '<div style="margin-top:0.5em">' \
                             '<div style="font-weight: bold">{}</div>' \
                             '<div>{}</div>' \
                             '<div style="color: #0096ab">{}</div>' \
                             '<div>{}</div>' \
                             '</div>'\
            .format(trans.title, trans.definition,
                    _join(trans.translations), trans.example)
    return '<div style="color:#444;font-style:italic">{}</div>' \
           '<div style="color:#e84427">&frasl;{}&frasl;</div>' \
           '<div>{}</div>' \
           '<div style="margin-top:1.25em">' \
           '<a href="{}">See more on dictionary.cambridge.org</a>' \
           '</div>' \
        .format(_join(note.pos_list), note.transcription,
                translations_html, note.url)


def print_note(note):
    """Print note to terminal"""
    print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + note.word)
    print(colorama.Style.BRIGHT + _join(note.pos_list))
    print(colorama.Style.BRIGHT + colorama.Fore.RED + note.transcription)
    for trans in note.translations:
        if trans.title:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + trans.title)
        print(colorama.Fore.LIGHTGREEN_EX + trans.definition)
        print(colorama.Fore.CYAN + colorama.Style.BRIGHT + _join(trans.translations))
        if trans.example:
            print(colorama.Fore.GREEN + trans.example)


def _fetch_data(word, src_lang, dst_lang):
    """Fetch data for parsing"""

    url, bs = _do_query(word, src_lang, dst_lang)
    title = _get_page_title(bs)

    # check derivation form. If title contains special symbols
    # then it is not dictionary form of query word and so we should
    # extract it from page and fetch translation for that dictionary form
    if not _is_dictionary_form(title):
        derived = re.search(r'“([^”]*)”', title).group(0)
        derived = derived[1:-1]
        print('"{}" is derivation from "{}". Search it.'.format(word, derived))
        url, bs = _do_query(derived, src_lang, dst_lang)
        title = _get_page_title(bs)
        # if we can't get dictionary form when we can't parse page
        if not _is_dictionary_form(title):
            raise Exception("Can't find dictionary form for {}".format(title))

    return url, bs, title


def _get_page_title(bs):
    return bs.find(class_='di-title').text


def _do_query(query_word, src_lang, dst_lang):
    query_url = _CAMBRIDGE_QUERY_URL.format(
        src=src_lang, dst=dst_lang, word=query_word)
    with urllib.request.urlopen(query_url) as response:
        encoding = response.headers.get_content_charset()
        html = response.read().decode(encoding)
        return query_url, BeautifulSoup(html, 'html.parser')


def _is_dictionary_form(string):
    # dictionary form doesn't contains any special symbol.
    # It's single word
    return re.match(r'\A[\w]+\Z', string)


def _join(string_list):
    """Join string list with comma"""
    return ", ".join(string_list)