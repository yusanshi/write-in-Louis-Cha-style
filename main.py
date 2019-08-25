from train import train
from apply import apply
from pathlib import Path
from config import MODEL_PATH, LOG_PATH
import os
import shutil


def main(beginning, num_of_chars, force_retrain=False):
    if force_retrain:
        if Path(MODEL_PATH).is_dir():
            shutil.rmtree(MODEL_PATH)

    if Path(LOG_PATH).is_dir():
        shutil.rmtree(LOG_PATH)

    if not Path(MODEL_PATH).is_dir():  # not exists
        os.mkdir(MODEL_PATH)

    if not os.listdir(MODEL_PATH):  # blank
        train()

    print(beginning + ' ' + apply(beginning, num_of_chars))


if __name__ == '__main__':
    main('那长须老者满脸得色，微微一笑', 1000)
