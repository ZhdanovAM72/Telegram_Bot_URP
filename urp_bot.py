#!/usr/bin/python

# Это пройтой бот с информацией для сотрудников.
# Создан для УРП.

import telebot

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['Старт'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

#кнопки помощи
@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website = types.KeyboardButton('Сайт_компании')
    start = types.KeyboardButton('start')
    can = types.KeyboardButton('info')
    markup.add(website,start,can)
    bot.send_message(message.chat.id, 'Используйте кнопки бота', reply_markup=markup)

bot.polling(none_stop=True)
