from train import train
from apply import apply
from pathlib import Path
from config import MODEL_PATH, CHECKPOINT_PATH
import os
import shutil


def main(beginning, num_of_chars, force_retrain=False, with_checkpoint=False, from_checkpoint=False):
    if force_retrain:
        if Path(MODEL_PATH).is_dir():
            shutil.rmtree(MODEL_PATH)

    if force_retrain or with_checkpoint:
        if Path(CHECKPOINT_PATH).is_dir():
            shutil.rmtree(CHECKPOINT_PATH)

    if not Path(MODEL_PATH).is_dir():  # not exists
        os.mkdir(MODEL_PATH)

    if not os.listdir(MODEL_PATH):  # blank
        train(with_checkpoint)

    print(beginning + ' ' + apply(beginning, num_of_chars, from_checkpoint))


if __name__ == '__main__':
    main('', 1000)
