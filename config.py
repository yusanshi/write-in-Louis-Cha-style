MODEL_PATH = 'saved_model'
LOG_PATH = 'log'
JS_PATH = 'tfjs'
SEQ_LENGTH = 100
EPOCHS = 100
BATCH_SIZE = 64
EMBEDDING_DIM = 256
RNN_UNITS = 512
LEARNING_RATE = 0.001
TEMPERATURE = 0.8  # bigger value means bigger randomness, and vice versa

# The actual quantity of data is the smaller of quantities decided by the two NUM
BOOK_NUM = 1  # None for all books (used together with LINE_NUM)
LINE_NUM = None  # None for all lines (used together with BOOK_NUM)
