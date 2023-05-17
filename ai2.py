import tensorflow as tf
import numpy as np
import os
from variables import CHECKPOINT_DIR
from variables import BATCH_SIZE, BUFFER_SIZE, EMBEDDING_DIM, RNN_UNITS


CHECKPOINT_PREFIX = os.path.join(CHECKPOINT_DIR, "ckpt_{epoch}")

last_epoch = 0
# проверяем, есть ли файл с номером последней эпохи
if os.path.exists(os.path.join(CHECKPOINT_DIR, "last_epoch.txt")):
    with open(os.path.join(CHECKPOINT_DIR, "last_epoch.txt"), "r") as f:
        last_epoch = int(f.read())

# Загружаем датасет
path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# Создаем словарь символов
vocab = sorted(set(text))
char2idx = {u: i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)

# Создаем обучающие данные
def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

text_as_int = np.array([char2idx[c] for c in text])

char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

sequences = char_dataset.batch(2, drop_remainder=True).map(split_input_target)

dataset = sequences.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

# Создаем модель
def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model

model = build_model(vocab_size=len(vocab), embedding_dim=EMBEDDING_DIM, rnn_units=RNN_UNITS, batch_size=BATCH_SIZE)

# Определяем функцию потерь и оптимизатор
def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

model.compile(optimizer='adam', loss=loss)

# Создаем коллбэк для сохранения модели
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PREFIX, save_weights_only=True)
model.load_weights(tf.train.latest_checkpoint(CHECKPOINT_DIR))

# Обучаем модель, указывая параметр initial_epoch равным last_epoch
history = model.fit(dataset, epochs=50, callbacks=[checkpoint_callback], initial_epoch=last_epoch)

# Сохраняем номер последней эпохи
with open(os.path.join(CHECKPOINT_DIR, "last_epoch.txt"), "w") as f:
    f.write(str(last_epoch + 30)) # увеличиваем на 30, чтобы соответствовать количеству эпох, указанных в history

# Генерируем текст
def generate_text(model, start_string):
    num_generate = 1000
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)
    text_generated = []
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)

        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))

# Загружаем модель из последнего чекпойнта
model = build_model(vocab_size=len(vocab), embedding_dim=EMBEDDING_DIM, rnn_units=RNN_UNITS, batch_size=1)
model.load_weights(tf.train.latest_checkpoint(CHECKPOINT_DIR))

# # Пример использования модели
# print(generate_text(model, start_string=u'Hello, how are you doing today?'))

