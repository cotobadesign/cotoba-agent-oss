import json
import logging
import os
import sys
import traceback

from statistics import mean

import hydra
from tqdm import tqdm

from util import (
    get_relative_path,
    get_result,
    load_model
)


logger = logging.getLogger(__name__)


def _print(msg):
    # print(msg)
    logger.info(msg)


def _main(cfg):
    try:
        with open(cfg.test.data) as f:
            test_data = json.load(f)
        test_data = test_data[cfg.test.key]
        intent_rec, slot_rec = load_model(cfg)
        if intent_rec is None:
            logger.info('model for intent is not found.')
        if slot_rec is None:
            logger.info('model for slot is not found.')
        if intent_rec is None and slot_rec is None:
            raise Exception('No model has been loaded.')
        test(test_data, intent_rec, slot_rec, threshold=0.5)
    except Exception as err:
        print(traceback.format_tb(err.__traceback__), file=sys.stderr)
        sys.exit(1)


def get_valid_labels(data):
    intents = set()
    slots = set()
    for d in data:
        if 'intent' in d:
            for intent in d['intent']:
                intents.add(intent)
        if 'slot' in d:
            for slot in d['slot']:
                slots.add(slot['type'])
    return intents, slots


def update_intent_result_summary(intent_result_summary,
                                 correct, predict,
                                 valid_intents):
    for intent in correct:
        if intent not in intent_result_summary:
            intent_result_summary[intent] = {'tp': 0, 'fp': 0, 'all': 0}
        intent_result_summary[intent]['all'] += 1
    for res in predict:
        intent = res['intent']
        if intent not in valid_intents:
            continue
        if intent not in intent_result_summary:
            intent_result_summary[intent] = {'tp': 0, 'fp': 0, 'all': 0}
        if intent in correct:
            intent_result_summary[intent]['tp'] += 1
        else:
            intent_result_summary[intent]['fp'] += 1


def update_slot_result_summary(slot_result_summary,
                               correct, predict,
                               valid_slots):
    for slot in correct:
        sl = slot['type']
        if sl not in slot_result_summary:
            slot_result_summary[sl] = {'tp': 0, 'fp': 0, 'all': 0}
        slot_result_summary[sl]['all'] += 1
    for res in predict:
        slt = res['slot']
        if slt not in valid_slots:
            continue
        st = res['startOffset']
        ed = res['endOffset']
        flag = False
        for sl in correct:
            t_slt = sl['type']
            t_st = sl['start']
            t_ed = sl['end']
            if slt == t_slt and st == t_st and ed == t_ed:
                flag = True
                break
        if slt not in slot_result_summary:
            slot_result_summary[slt] = {'tp': 0, 'fp': 0, 'all': 0}
        if flag:
            slot_result_summary[slt]['tp'] += 1
        else:
            slot_result_summary[slt]['fp'] += 1


def test(test_data, intent_rec, slot_rec, threshold=0.5):
    valid_intents, valid_slots = get_valid_labels(test_data)
    intent_result_summary = {}
    slot_result_summary = {}
    for t_data in tqdm(test_data):
        text = t_data['text']
        result = get_result(text, intent_rec, slot_rec, threshold)
        """ intent """
        intent_result = result['intents']
        update_intent_result_summary(intent_result_summary,
                                     t_data['intent'],
                                     intent_result,
                                     valid_intents)
        """ for slot """
        slot_result = result['slots']
        update_slot_result_summary(slot_result_summary,
                                   t_data['slot'],
                                   slot_result,
                                   valid_slots)
    _print('Result of intent:')
    print_score(intent_result_summary)
    _print('Result of slot:')
    print_score(slot_result_summary)


def calc_prec_rec_f(tp, fp, fn):
    f, prec, rec = 0., 0., 0.
    if tp != 0:
        prec = tp / (fp + tp)
        rec = tp / (fn + tp)
        f = 2 * prec * rec / (prec + rec)
    return f, prec, rec


def print_score(result):
    f_measures = []
    tp, fp, fn = 0, 0, 0
    for label in result:
        tp_ = result[label]['tp']
        tp += tp_
        fp_ = result[label]['fp']
        fp += fp
        fn_ = result[label]['all'] - tp_
        fn += fn_
        f, prec, rec = calc_prec_rec_f(tp_, fp_, fn_)
        msg = f'{label}\tprec:{prec:.3f}\trec:{rec:.3f}\tf:{f:.3f}'
        _print(msg)
        f_measures.append(f)
    macro_average = mean(f_measures)
    _print(f'Macro average F-measure: {macro_average:.3f}')
    f_micro, prec_micro, rec_micro = calc_prec_rec_f(tp, fp, fn)
    _print(f'Micro average F-measure: {f_micro:.3f}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python run.py [your model_test.yaml]', file=sys.stderr)
        sys.exit(0)
    config_path = sys.argv.pop()
    if not os.path.exists(config_path):
        print(f'{config_path} is not found.', file=sys.stderr)
        sys.exit(0)

    rel_path = get_relative_path(config_path)
    main = hydra.main(config_path=rel_path, strict=False)(_main)
    main()
