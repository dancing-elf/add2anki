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

    if not args.output:
        print(colorama.Fore.YELLOW + 'csv file not selected')

    print_invitation()
    for line in sys.stdin:
        word = line.strip()
        try:
            note = cambridge.translate(word, args.src_lang, args.dst_lang)
            cambridge.print_note(note)
            if args.output:
                with open(args.output, 'a+') as output_file:
                    print(note.word + "\t" + cambridge.to_html(note),
                          file=output_file)
        except:
            print(colorama.Fore.RED + 'Error while handle {}: '.format(word),
                  sys.exc_info())
        print_invitation()


def print_invitation():
    print()
    print('search for: ', end='')


if __name__ == '__main__':
    sys.exit(add2anki())