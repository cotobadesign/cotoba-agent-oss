import json
import logging
import time
import os
import sys

import hydra

from util import (
    get_relative_path,
    get_result,
    load_model
)


logger = logging.getLogger(__name__)


def _main(cfg):
    intent_rec, slot_rec = load_model(cfg)
    if intent_rec is None:
        logger.info('model for intent is not founded.')
    if slot_rec is None:
        logger.info('model for slot is not founded.')
    if intent_rec is None and slot_rec is None:
        logger.error('No model has been loaded.')
        sys.exit(1)
    while True:
        print('>> please input text and push enter key.')
        text = input()
        if len(text) == 0:
            continue
        start = time.time()
        res = get_result(text, intent_rec, slot_rec)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        process_time = time.time() - start
        print('f{process_time} sec.')
        logger.info(json.dumps(res, ensure_ascii=False))
        logger.info(f'{process_time} sec')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python run.py [your model_path.yaml]', file=sys.stderr)
        sys.exit(0)
    config_path = sys.argv.pop()
    if not os.path.exists(config_path):
        print(f'{config_path} is not found.', file=sys.stderr)
        sys.exit(0)

    rel_path = get_relative_path(config_path)
    main = hydra.main(config_path=rel_path, strict=False)(_main)
    main()
