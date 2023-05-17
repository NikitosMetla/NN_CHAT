from aiogram import types

#токен бота
Bot_token = '6251396122:AAFhRwz0zTuXpk4oHLndt8UoLrRHmeYpjic'

# айди приветствующего стикера
sticker_id = 'CAACAgIAAxkBAAEHPahjwbzlOsXIHVlQguOW4s9bPK9-sAACCAADa-18CjWBoH9uCkN_LQQ'

#клавиатуры для бота
NN_buttons = ["Trololo_GPT🤖", "Stone🪨, Scissors✂️, Paper📄", '❌Cancel']
choise_NN = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in NN_buttons:
    choise_NN.add(button)


continue_game_buttons = ["Yes☑️", "❌No", '❌Cancel']
continue_game = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*continue_game_buttons)

SSC_buttons1 = ["Stone🪨", "Scissors✂️", "Paper📄"]
SSC_buttons2 = ['❌Cancel', "My stats💪"]
choise_SSC = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*SSC_buttons1)
for i in SSC_buttons2[::-1]:
    choise_SSC.add(i)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['✅Yes', '❌No', 'My requests📂']
keyboard.add(*buttons)

keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons3 = ['🗑Clean history of my requests', '▶️Start communication with Trololo_GPT']
keyboard3.add(*buttons3)

keyboard5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons5 = ['▶️Start communication with Trololo_GPT', '❌Cancel']
keyboard5.add(*buttons5)

keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True).add("My requests📂")
keyboard2.add("❌Complete")

keyboard_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True).add('❌Cancel')

#путь к проекту
CHECKPOINT_DIR = r"C:\Users\romaz\Desktop\pythonProject2"

#константы для TROLOLO_GPT
BATCH_SIZE = 64
BUFFER_SIZE = 10000
EMBEDDING_DIM = 256
RNN_UNITS = 1024