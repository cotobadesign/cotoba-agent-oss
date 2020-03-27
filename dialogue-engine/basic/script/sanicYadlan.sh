
#! /bin/sh
clear
export PYTHONPATH=PYTHONPATH=:../../src 
python3 -m programy.clients.restful.yadlan.sanic.client  --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml --stdoutlog True

