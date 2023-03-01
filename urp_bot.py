# Это пройтой бот с информацией для сотрудников.
# Создан для УРП.

import telebot
from telebot import types
#from .api import Apy


API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn01 = types.KeyboardButton('Информация о боте')
    btn02 = types.KeyboardButton('Главное меню')
    markup.add(btn01, btn02)
    mess = (f'Привет, <b>{message.from_user.first_name} '
            f'{message.from_user.last_name}</b>! '
             'Я расскажу тебе о нефтесервисных активах! '
             'выберите интересующую вас тему в меню.')
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

# stop
@bot.message_handler(commands=['stp'])
def stop_command(message):
    bot.send_message(message.chat.id, 'OK, stop...')
    print("OK, stop...")
    bot.stop_polling()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # main menu
    if message.text == 'Главное меню' or message.text == '🔙 Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('О компании')
        btn2 = types.KeyboardButton('Адаптация')
        btn3 = types.KeyboardButton('Карьерное развитие')
        btn4 = types.KeyboardButton('Регулярная оценка')
        btn5 = types.KeyboardButton('Обучение')
        btn6 = types.KeyboardButton('Стажировка')
        btn7 = types.KeyboardButton('ДМС и РВЛ')
        btn8 = types.KeyboardButton('Молодежная политика')
        btn9 = types.KeyboardButton('Обратная связь')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(message.from_user.id, "Добро пожаловать в главное меню чат-бота", reply_markup=markup)
        bot.send_message(message.from_user.id, 'Выберите интересующий вас раздел')
    
    elif message.text == 'О компании' or message.text == '🔙 вернуться в раздел О компании':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_about_1 = types.KeyboardButton('🔙 Главное меню')
        btn_about_2 = types.KeyboardButton('Выбрать ДО')
        btn_about_3 = types.KeyboardButton('Наши корпоративные ценности')
        btn_about_4 = types.KeyboardButton('Сервисы для сотрудников')
        btn_about_5 = types.KeyboardButton('Новостная лента')
        markup.add(btn_about_2, btn_about_3, btn_about_4, btn_about_5, btn_about_1)
        bot.send_message(message.from_user.id, "⬇ О компании", reply_markup=markup)

    elif message.text == 'Выбрать ДО' or message.text == '🔙 вернуться в раздел Выбрать ДО':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('ГПН НС')
        btn_do_3 = types.KeyboardButton('ГПН ЭС')
        btn_do_4 = types.KeyboardButton('ННГГФ')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        bot.send_message(message.from_user.id, "⬇ Выбрать ДО", reply_markup=markup)

    elif message.text == 'ГПН ЭС' or message.text == '🔙 вернуться в раздел ГПН ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ЭС')
        btn_es_3 = types.KeyboardButton('Структура ЭС')
        btn_es_4 = types.KeyboardButton('Контакты ЭС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        bot.send_message(message.from_user.id, "⬇ ГПН ЭС", reply_markup=markup)

    # ГПН ЭС
    elif message.text == 'История ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('data/gpn_es/about_us.pptx', 'rb')
        markup.add(btn_history_es)
        bot.send_document(message.chat.id, doc_es, caption = 'История ООО "Газпромнефть Энергосистемы"', parse_mode="html")
    
    # elif message.text == 'Адаптация':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Карьерное развитие':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Регулярная оценка':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Обучение':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Стажировка':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'ДМС и РВЛ':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Молодежная политика':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    # elif message.text == 'Обратная связь':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')
    
    else:
        message.text == 'Информация о боте'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_info_0 = types.KeyboardButton('Главное меню')
        markup.add(btn_info_0)
        bot.send_message(message.from_user.id, "Переходи в главное меню и узнай самую важную информацию о нефтесервисных активах!", parse_mode='html', reply_markup=markup)   

# сайт
# @bot.message_handler(commands=['website'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Открыть сайт",
#                url="http://gazpromneftenergysystems.ru"))
#     bot.send_message(message.chat.id, 'Откройте сайт', reply_markup=markup)


# ответ на картинку
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'У меня нет глаз, '
                                      'я не понимаю что на этой картинке'
                                      'Давай продолжим работать в меню.')


bot.polling(none_stop=True, interval=0)
