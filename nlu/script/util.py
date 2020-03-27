import json
import os
import sys
import traceback

import hydra
import spacy


def get_relative_path(path):
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(path)
    path = os.path.relpath(path, base)
    return path


def _load_model(model_dir):
    model = None
    try:
        meta = os.path.join(model_dir, 'meta.json')
        if os.path.exists(meta):
            model = spacy.load(model_dir)
    except Exception as err:
        print(traceback.format_tb(err.__traceback__), file=sys.stderr)
    finally:
        return model


def load_best_model(model_dir):
    ret = None
    if not os.path.isdir(model_dir):
        return ret
    min_loss = sys.float_info.max
    for filename in os.listdir(path=model_dir):
        model_path = os.path.join(model_dir, filename)
        if os.path.isdir(model_path):
            meta = os.path.join(model_path, 'meta.json')
            with open(meta) as f:
                loss = json.load(f)['score']['loss']
            if min_loss > loss:
                min_loss = loss
                ret = model_path
    if ret:
        ret = spacy.load(ret)
    return ret


def get_path_by_original_cwd(rel_path):
    org_cwd = hydra.utils.get_original_cwd()
    return os.path.join(org_cwd, rel_path)


def get_intente_result(intents, threshold=0.5):
    intent_result = []
    if 'cats' not in intents:
        return intent_result
    for intent in intents['cats']:
        score = intents['cats'][intent]
        if score > threshold:
            intent_result.append(
                {'intent': intent, 'score': score})
    return intent_result


def get_slot_result(slots, text):
    slot_result = []
    if 'ents' not in slots:
        return slot_result
    for slot in slots['ents']:
        start = slot['start']
        end = slot['end']
        label = slot['label']
        entity = text[start:end]
        slot_result.append({
            'slot': label,
            'startOffset': start,
            'endOffset': end,
            'entity': entity,
            'score': 1.0  # This model cannot use the score.
        })
    return slot_result


def get_result(text, intent_rec, slot_rec, threshold=0.5):
    intent_result = []
    slot_result = []
    if intent_rec:
        intents = intent_rec(text).to_json()
        intent_result = get_intente_result(intents, threshold)
    if slot_rec:
        slots = slot_rec(text).to_json()
        slot_result = get_slot_result(slots, text)
    return {'text': text, 'intents': intent_result, 'slots': slot_result}


def load_model(cfg):
    intent_path = get_path_by_original_cwd(cfg.model.intent)
    intent_rec = _load_model(intent_path)
    slot_path = get_path_by_original_cwd(cfg.model.slot)
    slot_rec = _load_model(slot_path)
    return intent_rec, slot_rec


def write_json(filename, obj):
    with open(filename, 'w') as f:
        json.dump(obj, f, ensure_ascii=False)
