from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'iconfile': 'appicon.icns', 
    'includes': ['PyQt5']
}

setup(
    app=APP,
    name='Hangman',
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)