# add2anki

## Description
Tools for word translation and adding it to csv file for Anki

At this point supported only creation of csv file with tab delimiter from
file with words for translation.

## Requirements
Python 3.5

## Running
From project root run:
pip install -r requirements.txt
python setup.py install
Then run:
add2anki -from=src_lang -to=dst_lang -out=path_to_csv_file
or for creating csv file for import:
csv4anki -in=path_to_input -out=path_to_output -from=src_lang -to=dst_lang