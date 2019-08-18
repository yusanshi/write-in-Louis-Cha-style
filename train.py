from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
import os
import io
import re
import time
import jieba
import pprint
import pickle
import itertools
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from tensorflow import keras
from tensorflow.keras import layers
from collections import Counter
from config import MODEL_PATH, DATA_NUM, SEQ_LENGTH, EPOCHS, BATCH_SIZE, EMBEDDING_DIM, RNN_UNITS, LEARNING_RATE


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        layers.Embedding(vocab_size + 1, embedding_dim,
                         batch_input_shape=[batch_size, None]),
        layers.LSTM(rnn_units,
                    return_sequences=True,
                    stateful=True,
                    recurrent_initializer='glorot_uniform'),
        layers.Dense(vocab_size)
    ])
    return model


def loss(labels, logits):
    return keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


def train():

    # Prepare data
    path_to_zip = keras.utils.get_file(
        'Louis_Cha_novels.zip', origin='https://yun.yusanshi.com/TF_datasets/Louis_Cha_novels.zip', extract=True)
    path_to_txt = os.path.join(os.path.dirname(path_to_zip), 'novels')

    def no_invalid_chars(s):
        fil = re.compile(
            u'[0-9a-zA-Z\u4e00-\u9fa5.,…，。、：；【】〈〉（）《》<>＋！%？— ·~‘’“” ]+', re.UNICODE)
        s = fil.sub('', s)
        return s == ''

    lines = []
    for file in os.listdir(path_to_txt):
        if os.path.splitext(file)[-1] == '.txt':
            with open(os.path.join(path_to_txt, file), 'r', encoding='utf-8') as f:
                lines.extend([l.strip() for l in f.readlines() if len(
                    l.strip()) > 0 and no_invalid_chars(l.strip())])

    lines = lines[:DATA_NUM]
    print('Lines num: %d' % len(lines))
    lines = [' '.join([l for l in list(jieba.cut(l)) if l != ' '])
             for l in lines]
    text = ' <br> '.join(lines)

    def tokenize(text):
        lang_tokenizer = keras.preprocessing.text.Tokenizer(filters='')
        lang_tokenizer.fit_on_texts(text)
        tensor = lang_tokenizer.texts_to_sequences(text)
        return tensor, lang_tokenizer

    tensor, tokenizer = tokenize([text])  # Must pass a list here!
    text_seq = tensor[0]
    text_length = len(text_seq)
    print('Fragments num: %d' % text_length)
    text_to_int = tokenizer.word_index
    int_to_text = tokenizer.index_word
    vocab_size = len(text_to_int)
    print('Vocabulary size: %d' % vocab_size)

    text_seq_dataset = tf.data.Dataset.from_tensor_slices(text_seq)
    text_seq_dataset_batched = text_seq_dataset.batch(
        SEQ_LENGTH+1, drop_remainder=True)

    def split_to_input_and_target(chunk):
        input_chunk = chunk[:-1]
        target_chunk = chunk[1:]
        return input_chunk, target_chunk

    dataset = text_seq_dataset_batched.map(split_to_input_and_target)
    dataset = dataset.shuffle(text_length//SEQ_LENGTH).batch(
        BATCH_SIZE, drop_remainder=True)

    # for inp, tar in dataset.take(1):
    #     print('Input' + str(inp))
    #     print('Target' + str(tar))
    #     print('Input first' + str(inp.numpy()[0]))
    #     print('Target first' + str(tar.numpy()[0]))

    model = build_model(vocab_size=vocab_size,
                        embedding_dim=EMBEDDING_DIM,
                        rnn_units=RNN_UNITS,
                        batch_size=BATCH_SIZE)
    # model.summary()
    model.compile(optimizer=keras.optimizers.Adam(
        learning_rate=LEARNING_RATE), loss=loss)

    model.fit(dataset, epochs=EPOCHS)

    # model.save(os.path.join(MODEL_PATH, 'model.h5'))

    def save_model(variables, models):
        for k, v in variables.items():
            with open(os.path.join(MODEL_PATH, k+'.pickle'), 'wb') as handle:
                pickle.dump(v, handle, protocol=pickle.HIGHEST_PROTOCOL)

        for k, v in models.items():
            v.save_weights(os.path.join(MODEL_PATH, k+'.ckpt'))

        print('Model saved in %s.' % MODEL_PATH)

    save_model(
        {
            'text_to_int': text_to_int,
            'int_to_text': int_to_text,
            'vocab_size': vocab_size
        },
        {
            'model': model
        }
    )


if __name__ == '__main__':
    train()
