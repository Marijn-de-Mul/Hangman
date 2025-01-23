#!/bin/bash

source .venv/bin/activate

arch -x86_64 python setup.py py2app
mv dist dist_mac_x86
