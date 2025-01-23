from setuptools import setup
import sys
import os

APP = ['main.py']
OPTIONS = {
    'iconfile': 'appicon.icns', 
    'includes': ['PyQt5']
}

install_requires = [
    'PyQt5'
]

if sys.platform == "darwin":
    setup(
        app=APP,
        name='Hangman',
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
        install_requires=install_requires
    )
elif sys.platform == "win32":
    from cx_Freeze import Executable
    from cx_Freeze import setup as cx_setup
    cx_setup(
        name='Hangman',
        options={'build_exe': {'includes': OPTIONS['includes']}},
        executables=[Executable('main.py', base=None, icon='appicon.ico')],
        install_requires=install_requires
    )