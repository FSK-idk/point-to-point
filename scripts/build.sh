#!/bin/bash

python -m venv ./.venv
. .venv/bin/activate
pip install -r requirements.txt
pyside6-rcc -o ./point_to_point/resource_rc.py ./point_to_point/resource.qrc
