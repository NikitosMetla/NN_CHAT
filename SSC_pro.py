import numpy as np
import tensorflow as tf
import os
from variables import CHECKPOINT_DIR

# Определяем словарь для преобразования выбора пользователя в численное значение
move_to_number = {"Stone🪨": 0, "Scissors✂️": 1, "Paper📄": 2}

# Определяем словарь для преобразования численного значения выбора модели в текстовое значение
number_to_move = {0: "Stone🪨", 1: "Scissors✂️", 2: "Paper📄"}

# Определяем функцию для преобразования истории ходов в массив numpy
def get_input_array(history):
    result = np.zeros((1, 9))
    for i in range(len(history)):
        result[0, i*3+history[i]] = 1
    return result

def my_model():
    if os.path.exists(os.path.join(CHECKPOINT_DIR, 'rps_model2.h5')):
        return tf.keras.models.load_model('rps_model2.h5')
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(9,)),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    # Компилируем нейронную сеть
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.save('rps_model2.h5')
    return model

def play_game(model, history, user_move):
    if user_move not in move_to_number:
        return "Некорректный ход"
    history.append(move_to_number[user_move])
    if len(history) > 3:
        history = history[-3:]
    if len(history) == 3:
        X = get_input_array(history)
    prediction = model.predict(X)[0]
    computer = np.argmax(prediction)
    user = move_to_number[user_move]
    if user == computer:
        return [f"Draw!\nYou choise the <b>{number_to_move[user]}</b>\nCumputer choise the <b>{number_to_move[computer]}</b>", 1]
    elif user == 0 and computer == 1:
        return [f"You are winning!\nYou choise the <b>{number_to_move[user]}</b>\nCumputer choise the <b>{number_to_move[computer]}</b>", 2]
    elif user == 1 and computer == 2:
        return [f"You are winning!!\nYou choise the <b>{number_to_move[user]}</b>\nCumputer choise the <b>{number_to_move[computer]}</b>", 2]
    elif user == 2 and computer == 0:
        return [f"You are winning!\nYou choise the <b>{number_to_move[user]}</b>\nCumputer choise the <b>{number_to_move[computer]}</b>", 2]
    else:
        return [f"You lose!\nYou choise the <b>{number_to_move[user]}</b>\nCumputer choise the <b>{number_to_move[computer]}</b>", 0]