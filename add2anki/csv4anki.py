"""Script to convert user's words to csv file that can be imported to Anki"""
import sys
import argparse
import add2anki.cambridge as cambridge


def csv4anki():
    """parse arguments and write data to csv"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-in', dest="input", help='File with new words')
    parser.add_argument('-out', dest="output", help='Output csv file with tab delimiter')
    parser.add_argument('-from', dest="src_lang", help='Source language')
    parser.add_argument('-to', dest="dst_lang", help='Destination language')

    args = parser.parse_args()

    with open(args.input) as input_file, open(args.output, 'a+') as output_file:
        for word in input_file:
            word = word.strip()
            if not word:
                continue
            print('translating "{}"'.format(word))
            note = cambridge.translate(word, args.src_lang, args.dst_lang)
            print(note.word + "\t" + cambridge.to_html(note), file=output_file)


if __name__ == '__main__':
    sys.exit(csv4anki())
