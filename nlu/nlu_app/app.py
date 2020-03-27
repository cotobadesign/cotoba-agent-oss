import json
import os
from logging import getLogger, StreamHandler, Formatter, INFO

from flask import request, Flask

from util import (
    _load_model,
    get_intente_result,
    get_slot_result,
)

logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sh = StreamHandler()
sh.setLevel(INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

logger.info('Strat: Model Loading.')
intent_rec = _load_model(os.environ['INTENT_MODEL_PATH'])
slot_rec = _load_model(os.environ['SLOT_MODEL_PATH'])
logger.info('End: Model loaded.')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_result(text, thre=0.5):
    intent_result = []
    slot_result = []
    if intent_rec:
        intents = intent_rec(text).to_json()
        intent_result = get_intente_result(intents, thre)
    if slot_rec:
        slots = slot_rec(text).to_json()
        slot_result = get_slot_result(slots, text)
    return {'text': text, 'intents': intent_result, 'slots': slot_result}


@app.route('/nlu', methods=['POST'])
def nlu():
    try:
        body = request.get_json()
        utterance = body['utterance']
        res = get_result(utterance)
    except Exception as err:
        error = str(err)
        return json.dumps(
            {'message': error}, ensure_ascii=False, indent=2), 500
    logger.info(json.dumps(res, ensure_ascii=False))
    return json.dumps(res, ensure_ascii=False, indent=2), 200


if __name__ == "__main__":
    app.run()
