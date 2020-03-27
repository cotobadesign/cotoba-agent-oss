
#! /bin/sh
clear
export PYTHONPATH=PYTHONPATH=:../../src 
python3 -m programy.clients.events.console.client --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml

