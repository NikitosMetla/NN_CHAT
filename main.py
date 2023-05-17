from aiogram import Bot, Dispatcher, types, executor
from variables import keyboard, keyboard3, keyboard5, sticker_id, keyboard2, Bot_token, choise_NN, choise_SSC,\
    continue_game, keyboard_cancel
import ai2
from SSC_pro import my_model, play_game, move_to_number
import json


with open("users_stat.json", "r") as users_stats:
    users_stats = json.load(users_stats)
new_users_stats = {}
for key in users_stats.keys():
    new_users_stats[int(key)] = users_stats.get(key)
users_stats = new_users_stats


with open("users.json", "r") as users:
    users = json.load(users)

new_users = {}
for key in users.keys():
    new_users[int(key)] = users.get(key)
users = new_users

bot = Bot(token=Bot_token, parse_mode='html')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer_sticker(sticker_id)
    await message.answer('👋🏿Hello, here you can choise one of the two neural networks', reply_markup=choise_NN)


@dp.message_handler(lambda message: message.text == "Stone🪨, Scissors✂️, Paper📄" or\
                    message.text == "Yes☑️")
async def start_gpt(message: types.Message):
    await message.reply("Ok, you must choise your move!", reply_markup=choise_SSC)


@dp.message_handler(lambda message: message.text == "Stone🪨" or\
                                    message.text == "Scissors✂️" or\
                                    message.text == "Paper📄")
async def start_gpt(message: types.Message):
    if message.from_user.id not in users_stats:
        users_stats[message.from_user.id] = {"wins":0, "loses":0, "draws":0, "history":[0, 1, 2]}
    history = users_stats.get(message.from_user.id)["history"][-2:]
    result = play_game(my_model(), history, message.text)
    if result[1] == 2:
        users_stats[message.from_user.id]["wins"] = users_stats.get(message.from_user.id)["wins"] + 1
    elif result[1] == 1:
        users_stats[message.from_user.id]["draws"] = users_stats.get(message.from_user.id)["draws"] + 1
    else:
        users_stats[message.from_user.id]["loses"] = users_stats.get(message.from_user.id)["loses"] + 1
    users_stats[message.from_user.id]["history"] = history
    with open("users_stat.json", "w") as users_stats2:
        json.dump(users_stats, users_stats2, indent=2)
    await message.reply(f"{result[0]}\n"
                        f"Do you want repeat game?", reply_markup=continue_game)


@dp.message_handler(lambda message: message.text == "My stats💪")
async def start(message: types.Message):
    if message.from_user.id not in users_stats:
        users_stats[message.from_user.id] = {"wins": 0, "loses": 0, "draws": 0, "history": [0, 1, 2]}
    await message.answer(f"✅Number of wins: <b>{users_stats.get(message.from_user.id)['wins']}</b>\n"
                         f"🤝Number of draws: <b>{users_stats.get(message.from_user.id)['draws']}</b>\n"
                         f"❌Number of loses: <b>{users_stats.get(message.from_user.id)['loses']}</b>\n"
                         f"Do you want repeat game?", reply_markup=continue_game)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Are you want to link with the help_team?')


@dp.message_handler(lambda message: message.text == 'Trololo_GPT🤖')
async def start(message: types.Message):
    await message.answer('OK, you will be using the Trololo_GPT🤖 as Telegram_Bot. Are you want to continue?',
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "❌No")
async def help(message: types.Message):
    await message.answer('You can choise one of the two neural networks', reply_markup=choise_NN)


@dp.message_handler(lambda message: message.text == '✅Yes' or\
                                    message.text == '▶️Start communication with Trololo_GPT')
async def start_gpt(message: types.Message):
    if users.get(message.from_user.id) is None:
        users[message.from_user.id] = []
    if len(users[message.from_user.id]) == 0:
        users[message.from_user.id].append([1])
    if len(users.get(message.from_user.id)) == 1:
        users[message.from_user.id][0] = [1]
        users[message.from_user.id].append([])
    else:
        users[message.from_user.id][0] = [1]
    with open("users.json", "w") as users_two:
        json.dump(users, users_two, indent=2)
    await message.reply("Nice, then <b>Trololo_GPT</b> ready to work with you! You can write your answer!",
                        reply_markup=keyboard_cancel)


@dp.message_handler(lambda message: message.text == '❌Cancel')
async def start_gpt(message: types.Message):
    await message.reply("Ok, if you will want use bot, write: /start", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'My requests📂')
async def start_gpt(message: types.Message):
    if (users[message.from_user.id][1] is not None) and len(users.get(message.from_user.id)[1]) > 0:
        user_list = users.get(message.from_user.id)[1]
        for i in range(len(user_list)):
            await message.reply(
                f"<b>Question</b>:\n\t\t\t\t<i>{user_list[i][0]['content']}</i>\n"
                f"<b>Answer</b>:\n\t\t\t\t<i>{user_list[i][1]['content']}</i>",
                reply_markup=keyboard3
            )
    else:
        await message.reply("You haven't got the requests. Ask ChatGpt anything and you will can see you request!",
                            reply_markup=keyboard5)


@dp.message_handler(lambda message: message.text == '🗑Clean history of my requests')
async def start_gpt(message: types.Message):
    users[message.from_user.id][1] = []
    with open("users.json", "w") as users_three:
        json.dump(users, users_three, indent=2)
    await message.reply("Your history was removed!", reply_markup=keyboard5)


@dp.message_handler(lambda message: message.text != '❌Complete' and message.text != "My requests📂")
async def start_gpt(message: types.Message):
    if users.get(message.from_user.id)[0] == [1]:
        if len(users[message.from_user.id][1]) > 2:
            users[message.from_user.id][1] = users.get(message.from_user.id)[1][-2:]
        messages = []
        messager = message.text
        chat_id = message.chat.id
        last_message = await bot.send_message(chat_id, "⌛️ Response preporation...")
        messages.append({"role": "user", "content": messager})
        reply = ai2.generate_text(ai2.model, start_string=message.text)
        messages.append({"role": "assistant", "content": reply})
        await message.answer(f"📌<b>Trololo_GPT</b>:\n{reply}", reply_markup=keyboard2)
        await bot.delete_message(chat_id=chat_id, message_id=last_message.message_id)
        users[message.from_user.id][1].append(messages)
        with open("users.json", "w") as users_four:
            json.dump(users, users_four, indent=2)
    else:
        await message.reply("I don't understand you, write /start")


@dp.message_handler(lambda message: message.text == '❌Complete')
async def start_gpt(message: types.Message):
    if users[message.from_user.id] is not None:
        users[message.from_user.id][0] = [0]
        with open("users.json", "w") as users_five:
            json.dump(users, users_five, indent=2)
    await message.reply("⭕️Trololo_GPT was completed his work. If you want to use the chat, write /start",
                        reply_markup=types.ReplyKeyboardRemove())

    
if __name__ == '__main__':
    executor.start_polling(dp)