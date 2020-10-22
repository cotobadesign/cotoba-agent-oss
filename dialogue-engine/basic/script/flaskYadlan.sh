
#! /bin/sh
clear
export PYTHONPATH=PYTHONPATH=:../storage/extensions:../../src 
python3 -m programy.clients.restful.yadlan.flask.client  --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml --stdoutlog True --stderrlog True

