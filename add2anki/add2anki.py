"""Interactively translate and add words to Anki if needed"""
import sys
import argparse
import add2anki.cambridge as cambridge
import colorama


def add2anki():
    """Translate and add words to Anki if needed"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-from', dest='src_lang', help='Source language')
    parser.add_argument('-to', dest='dst_lang', help='Destination language')
    parser.add_argument('-deck', dest='deck', nargs='?', help='Destination deck')

    args = parser.parse_args()

    colorama.init(autoreset=True)

    print_invitation()
    for line in sys.stdin:
        word = line.strip()
        try:
            note = cambridge.translate(word, args.src_lang, args.dst_lang)
            cambridge.print_note(note)
        except:
            print('Error while handle {}: '.format(word), sys.exc_info())
        print_invitation()


def print_invitation():
    print()
    print('search for: ', end='')


if __name__ == '__main__':
    sys.exit(add2anki())