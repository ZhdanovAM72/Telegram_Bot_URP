#!/usr/bin/python

# Это пройтой бот с информацией для сотрудников.
# Создан для УРП.

import telebot
from telebot import types

API_TOKEN = '5958298312:AAHXm00wTnlftHdidKO5hdGpng7RE9_euck'
bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    website = types.KeyboardButton('Сайт_компании')
    start = types.KeyboardButton('/Старт')
    info = types.KeyboardButton('/info')
    markup.add(website, start, info)
    mess = (f'Привет, <b>{message.from_user.first_name} '
            f'{message.from_user.last_name}</b>!')
    bot.send_message(message.chat.id, mess, parse_mode='html')


# сайт
@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть сайт",
               url="http://gazpromneftenergysystems.ru"))
    bot.send_message(message.chat.id, 'Откройте сайт', reply_markup=markup)


# информация для пользователя
@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message, 'Я расскажу тебе о нефтесервисных активах!')


# ответ на картинку
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'У меня нет глаз, '
                                      'я не понимаю что на этой картинке(')


# stop
@bot.message_handler(commands=['stp'])
def stop_command(message):
    bot.send_message(message.chat.id, 'OK, stop...')
    print("OK, stop...")
    bot.stop_polling()


bot.polling(none_stop=True)
