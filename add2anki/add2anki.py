"""Interactively translate and add words to csv file if needed"""
import argparse
import sys
import tempfile
import urllib

import colorama
import pygame

import add2anki.cambridge as cambridge


def add2anki():
    """Translate and add words to csv file if needed"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-from', dest='src_lang',
                        help='Source language', required=True)
    parser.add_argument('-to', dest='dst_lang',
                        help='Destination language', required=True)
    parser.add_argument('-out', dest='output', nargs='?',
                        help='Destination csv file')
    args = parser.parse_args()

    colorama.init(autoreset=True)

    note = None
    _print_invitation()
    for line in sys.stdin:
        word = line.strip()
        if not word:
            pass
        elif word == 'h':
            _handle_help()
        elif word == 'q':
            sys.exit(0)
        elif word == 'a':
            _handle_add(note, args.output)
        elif word == 's':
            _handle_sound(note)
        else:
            note = _handle_word(word, args.src_lang, args.dst_lang)
        _print_invitation()


def _print_invitation():
    """Print invitation for user input"""
    print()
    print('Type command or word for translation. '
          'Type "h" for list of possible commands')
    print('>>> ', end='')


def _handle_help():
    """Display help"""
    print('h display this help')
    print('q exit from add2anki')
    print('a add note to csv file')
    print('s play sound for last word')


def _handle_add(note, csv_file):
    """Add note to csv file"""
    if not note:
        _warn_none_note()
        return
    if not csv_file:
        print(colorama.Fore.YELLOW + 'csv file not selected')
        return
    with open(csv_file, 'a+') as output_file:
        print(note.word + "\t" + cambridge.to_html(note),
              file=output_file)


def _handle_sound(note):
    """Play sound for note"""
    if not note:
        _warn_none_note()
        return
    with tempfile.NamedTemporaryFile() as temp:
        urllib.request.urlretrieve(note.pronunciation, temp.name)
        _play_audio(temp.name)


def _handle_word(word, src_lang, dst_lang):
    """Translate word and print it to terminal"""
    note = None
    try:
        note = cambridge.translate(word, src_lang, dst_lang)
        cambridge.print_note(note)
    except:
        print(colorama.Fore.RED + 'Error while handle {}: '.format(word),
              sys.exc_info())
    return note


def _play_audio(path):
    """Play sound with pygame"""
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    audio = pygame.mixer.Sound(path)
    audio.play()


def _warn_none_note():
    print('There is no successfully translated word')