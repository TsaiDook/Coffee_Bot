import telebot
from telebot import types  # для указание типов
from keyboa import Keyboa
import config
import pandas as pd

# не знаю, насколько круто считывать данные сразу, но кажется логичным
bot = telebot.TeleBot(config.token)
users_data = pd.read_csv('users.csv', index_col=0)
events_data = pd.read_csv('events.csv', index_col=0)


# для добавления юзера
def add_user(message):
    global users_data
    user_id = message.from_user.id
    if user_id not in users_data.tg_id.values:
        append_df = pd.DataFrame([[user_id, message.from_user.username, False, None, None, None]],
                                 columns=list(users_data))
        users_data = users_data.append(append_df)
        users_data.to_csv('users.csv')


@bot.message_handler(commands=['start'])
def start(message):
    add_user(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
    markup.add(*buttons)
    bot.send_message(message.chat.id,
                     text=f"Привет, {message.from_user.username}! {config.intro_text}",
                     reply_markup=markup)


# не понимаю, как получить, какую кнопку тыкнули с клавы...
@bot.message_handler(content_types=['text'])
def communicate(message):
    if message.text == "Найти похожие события":
        bot.send_message(message.chat.id, text="Опиши мне его!")
    elif message.text == "Создать событие":
        bot.send_message(message.chat.id, text="Опиши событие, которое хочешь создать!")

    elif message.text == "Найти похожих юзеров":
        if users_data[users_data.tg_id == message.from_user.id].push_data.values[0]:
            bot.send_message(message.chat.id, "Ща как сделаю мэтч!")
        else:
            bot.send_message(message.chat.id, "Сначала необходимо ввести информацию о себе!")

    elif message.text == 'Рассказать о себе':
        if users_data[users_data.tg_id == message.from_user.id].push_data.values[0]:
            bot.send_message(message.chat.id, "Хотите изменить данные о себе?")
        else:
            bot.send_message(message.chat.id, "Давай начнем!")
            users_data.loc[users_data.tg_id == message.from_user.id, 'data'] = True
            # for user_attr, bot_phrase in config.user_attributes.items():
            #     bot.send_message(message.chat.id, bot_phrase)
            #     users_data.loc[users_data.tg_id == message.from_user.id, user_attr] = message.text
            keyboard = Keyboa(items=config.genders)
            bot.send_message(chat_id=message.chat.id, text="Choose your gender:", reply_markup=keyboard())
            print(keyboard.__call__())

            users_data.to_csv('users.csv')

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = (types.KeyboardButton(button_text) for button_text in config.start_buttons)
        markup.add(*buttons)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован :(")


bot.polling(none_stop=True)

# https://habr.com/ru/post/522720/ -- прикольный ввод
