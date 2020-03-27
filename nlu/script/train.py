import logging
import os
import sys

from pathlib import Path
from typing import cast

import hydra
import hydra.utils
import srsly
import torch

from omegaconf import Config

from camphr.cli.utils import check_nonempty
from camphr.lang.torch import TorchLanguage
from camphr.models import correct_model_config, create_model
from camphr.utils import resolve_alias
from camphr.cli.train import (
    train,
    set_seed,
    resolve_path,
    ALIASES
)


logger = logging.getLogger(__name__)

MUST_FIELDS = [
    "train.data.train",
    "train.data.val",
    [
        "model.ner_label",
        "model.textcat_label",
        "model.multitextcat_label",
        "model.pipeline.transformers_ner.labels",
        "model.pipeline.transformers_seq_classification.labels",
        "model.pipeline.transformers_multilabel_seq_classification.labels",
        "model.labels",
        "model.task",
    ],
    "model.lang.name",
]


def parse(cfg):
    assert isinstance(cfg, Config), cfg
    cfg = resolve_alias(ALIASES, cfg)
    check_nonempty(cfg, MUST_FIELDS)
    cfg = resolve_path(cfg)
    cfg.model = correct_model_config(cfg.model)
    return cfg


def _main(cfg):
    cfg = parse(cfg)
    if cfg.seed:
        set_seed(cfg.seed)
    org_cwd = hydra.utils.get_original_cwd()
    logger.info(cfg.pretty())
    nlp = cast(TorchLanguage, create_model(cfg.model))
    train_data = list(srsly.read_jsonl(
        os.path.join(org_cwd, cfg.train.data.train)))
    cfg.train.data.ndata = len(train_data)
    val_data = list(srsly.read_jsonl(
        os.path.join(org_cwd, cfg.train.data.val)))
    logger.info("output dir: {}".format(os.getcwd()))
    if torch.cuda.is_available():
        logger.info("CUDA enabled")
        nlp.to(torch.device("cuda"))
    savedir = Path.cwd() / "models"
    srsly.write_jsonl(Path.cwd() / f"train-data.jsonl", train_data)
    srsly.write_jsonl(Path.cwd() / f"val-data.jsonl", val_data)
    savedir.mkdir(exist_ok=True)
    train(cfg.train, nlp, train_data, val_data, savedir)


if __name__ == "__main__":
    from util import get_relative_path
    if len(sys.argv) != 2:
        print('python train.py [your train_(intent|slot).yaml]',
              file=sys.stderr)
        sys.exit(0)
    config_path = sys.argv.pop()
    if not os.path.exists(config_path):
        print(f'{config_path} is not found.', file=sys.stderr)
        sys.exit(0)
    rel_path = get_relative_path(config_path)
    main = hydra.main(config_path=rel_path, strict=False)(_main)
    main()
