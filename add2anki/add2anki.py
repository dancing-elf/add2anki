"""Interactively translate and add words to csv file if needed"""
import sys
import argparse
import add2anki.cambridge as cambridge
import colorama


def add2anki():
    """Translate and add words to csv file if needed"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-from', dest='src_lang', help='Source language')
    parser.add_argument('-to', dest='dst_lang', help='Destination language')
    parser.add_argument('-out', dest='output', nargs='?', help='Destination csv file')
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


def _warn_none_note():
    print('There is no successfully translated word')


if __name__ == '__main__':
    sys.exit(add2anki())