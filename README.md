# add2anki

## Description
Tool for adding automatically translated words to Anki

At this point supported only creation of csv file with tab delimiter from
file with words for translation.

## Requirements
Python 3.5

## Running
From project root run:
python -m add2anki.add2anki -from=src_lang -to=dst_lang
or for creating csv file for import:
python -m add2anki.csv4anki -in=path_to_input -out=path_to_output -from=src_lang -to=dst_lang