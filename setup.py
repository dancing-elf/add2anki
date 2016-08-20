from setuptools import setup

setup(
    name='add2anki',
    version='1.0',
    packages=['add2anki'],
    license="BSD",
    description='Tools for word translation and adding it to csv file for Anki',
    long_description=open('README.md').read(),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'add2anki=add2anki.add2anki:add2anki',
            'csv4anki=add2anki.csv4anki:csv4anki',
        ],
    },
)