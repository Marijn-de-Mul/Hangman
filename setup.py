from setuptools import setup
import sys
import os

APP = ['main.py']
OPTIONS = {
    'iconfile': 'appicon.icns', 
    'includes': ['PyQt5']
}

if sys.platform == "darwin":
    setup(
        app=APP,
        name='Hangman',
        options={'py2app': OPTIONS},
        setup_requires=['py2app']
    )
elif sys.platform == "win32":
    setup(
        name='Hangman',
        options={'build_exe': {'includes': OPTIONS['includes']}},
        executables=[Executable('main.py', base=None, icon='appicon.ico')]
    )
else:
    setup(
        name='Hangman',
        options={'build_exe': {'includes': OPTIONS['includes']}},
        executables=[Executable('main.py', base=None)]
    )