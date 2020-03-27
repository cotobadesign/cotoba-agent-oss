import json
import logging
import os
import random
import sys

import hydra
import srsly

from util import write_json

logger = logging.getLogger(__name__)


def get_sets(training_data):
    category_set = set()
    entity_set = set()
    for data in training_data:
        if 'intent' in data:
            for i in data['intent']:
                category_set.add(i)
        if 'slot' in data:
            for s in data['slot']:
                entity_set.add(s['type'])
    return category_set, entity_set


def _conv(data, category_set, entity_set):
    converted_data = []
    for d in data:
        text = d['text']
        ents = []
        cats = {}
        for slot in d['slot']:
            if slot['type'] in entity_set:
                ents.append(
                    (slot['start'], slot['end'], slot['type']))
        intents = [k for k in d['intent']]
        for i in category_set:
            if i in intents:
                cats[i] = 1.0
            else:
                cats[i] = 0.0
        converted_data.append(
            (text, {"entities": ents, "cats": cats})
        )
    return converted_data


def conv(cfg):
    original_cwd = hydra.utils.get_original_cwd()
    outdir = os.getcwd()
    filename = os.path.join(
        original_cwd, cfg.convert.input_file)
    num = cfg.convert.n_instances
    seed = cfg.convert.seed
    random.seed(seed)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    training_data = []
    val_data = []
    with open(filename) as f:
        j = json.load(f)
        for k in j:
            if k == 'training':
                training_data.extend(j[k])
            if k == 'validation':
                val_data.extend(j[k])
    if num > 0:
        if len(training_data) >= num:
            random.shuffle(training_data)
            training_data = training_data[:num]
        if len(val_data) >= num:
            random.shuffle(val_data)
            val_data = val_data[:num]
    category_set, entity_set = get_sets(training_data)
    converted_train_data = _conv(
        training_data, category_set, entity_set)
    converted_val_data = _conv(
        val_data, category_set, entity_set)
    srsly.write_jsonl(f'{outdir}/train.jsonl', converted_train_data)
    logger.info('size of training data: {}'.format(
        len(converted_train_data)))
    srsly.write_jsonl(f'{outdir}/val.jsonl', converted_val_data)
    logger.info('size of validation data: {}'.format(
        len(converted_train_data)))
    write_json(f'{outdir}/entities.json', list(entity_set))
    logger.info('size of slot labels: {}'.format(
        len(entity_set)))
    write_json(f'{outdir}/intents.json', list(category_set))
    logger.info('size of intent labels: {}'.format(
        len(category_set)))


if __name__ == '__main__':
    from util import get_relative_path
    if len(sys.argv) != 2:
        print('python convert.py [your convert.yaml]', file=sys.stderr)
        sys.exit(0)
    config_path = sys.argv.pop()
    if not os.path.exists(config_path):
        print(f'{config_path} is not found.', file=sys.stderr)
        sys.exit(0)
    rel_path = get_relative_path(config_path)
    main = hydra.main(config_path=rel_path, strict=False)(conv)
    main()
