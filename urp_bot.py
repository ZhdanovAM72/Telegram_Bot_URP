import telebot
from telebot import types
from settings import URP_BOT_TOKEN

API_TOKEN = URP_BOT_TOKEN
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
    bot.send_message(message.chat.id,
                     mess, parse_mode='html',
                     reply_markup=markup)


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
        bot.send_message(message.from_user.id,
                         "Добро пожаловать в главное меню чат-бота",
                         reply_markup=markup)
        bot.send_message(message.from_user.id,
                         'Выберите интересующий вас раздел')

    elif (message.text == 'О компании'
          or message.text == '🔙 вернуться в раздел О компании'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_about_1 = types.KeyboardButton('🔙 Главное меню')
        btn_about_2 = types.KeyboardButton('Выбрать ДО')
        btn_about_3 = types.KeyboardButton('Наши корпоративные ценности')
        btn_about_4 = types.KeyboardButton('Сервисы для сотрудников')
        btn_about_5 = types.KeyboardButton('Новостная лента')
        markup.add(
            btn_about_2,
            btn_about_3,
            btn_about_4,
            btn_about_5,
            btn_about_1
            )
        bot.send_message(
            message.from_user.id,
            "⬇ О компании",
            reply_markup=markup
            )

    elif (message.text == 'Выбрать ДО'
          or message.text == '🔙 вернуться в раздел Выбрать ДО'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('ГПН НС')
        btn_do_3 = types.KeyboardButton('ГПН ЭС')
        btn_do_4 = types.KeyboardButton('ННГГФ')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        bot.send_message(message.from_user.id, "⬇ Выбрать ДО", reply_markup=markup)

    # ГПН ЭС
    elif message.text == 'ГПН ЭС' or message.text == '🔙 вернуться в раздел ГПН ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ЭС')
        btn_es_3 = types.KeyboardButton('Структура ЭС')
        btn_es_4 = types.KeyboardButton('Контакты ЭС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        bot.send_message(message.from_user.id, "⬇ ГПН ЭС", reply_markup=markup)

    # ГПН ЭС история
    elif message.text == 'История ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('bot_data/presentations/history_gpn_es.pptx', 'rb')
        markup.add(btn_history_es)
        bot.send_document(message.chat.id, doc_es, caption = 'История ООО "Газпромнефть Энергосистемы"', parse_mode="html")

    # ГПН ЭС структура
    elif message.text == 'Структура ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('bot_data/presentations/structure_gpn_es.pptx', 'rb')
        markup.add(btn_structure_es)
        bot.send_document(message.chat.id, doc_es, caption = 'Структура компании ООО "Газпромнефть Энергосистемы"', parse_mode="html")

    # ГПН ЭС контакты
    elif message.text == 'Контакты ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('...bot_data/presentations/...', 'rb')
        markup.add(btn_structure_es)
        bot.send_document(message.chat.id, doc_es, caption = 'Контакты компании ООО "Газпромнефть Энергосистемы"', parse_mode="html")

    # ННГГФ
    elif message.text == 'ННГГФ' or message.text == '🔙 вернуться в раздел ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ННГГФ')
        btn_es_3 = types.KeyboardButton('Структура ННГГФ')
        btn_es_4 = types.KeyboardButton('Контакты ННГГФ')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        bot.send_message(message.from_user.id, "⬇ ННГГФ", reply_markup=markup)

    # ННГГФ история
    elif message.text == 'История ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('bot_data/presentations/404.pptx', 'rb')  # Заплатка
        markup.add(btn_history_es)
        bot.send_document(message.chat.id, doc_es, caption = 'История ННГГФ', parse_mode="html")

    # ННГГФ структура
    elif message.text == 'Структура ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_nnggf = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('bot_data/presentations/structure_gpn_nnggf.pptx', 'rb')
        markup.add(btn_structure_nnggf)
        bot.send_document(message.chat.id, doc_es, caption = 'Структура компании ННГГФ', parse_mode="html")

    # ННГГФ контакты
    elif message.text == 'Контакты ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('bot_data/presentations/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_es)
        bot.send_document(message.chat.id, doc_es, caption = 'Контакты компании ННГГФ', parse_mode="html")

    # ГПН НС
    elif message.text == 'ГПН НС' or message.text == '🔙 вернуться в раздел ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ГПН НС')
        btn_es_3 = types.KeyboardButton('Структура ГПН НС')
        btn_es_4 = types.KeyboardButton('Контакты ГПН НС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        bot.send_message(message.from_user.id, "⬇ ГПН НС", reply_markup=markup)

    # ГПН НС история
    elif message.text == 'История ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_ns = types.KeyboardButton('🔙 вернуться в раздел ГПН НС')
        doc_ns = open('bot_data/presentations/history_gpn_es.pptx', 'rb')
        markup.add(btn_history_ns)
        bot.send_document(message.chat.id, doc_ns, caption = 'История ГПН НС', parse_mode="html")

    # ГПН НС структура
    elif message.text == 'Структура ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_nnggf = types.KeyboardButton('🔙 вернуться в раздел ГПН НС')
        doc_es = open('bot_data/presentations/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_nnggf)
        bot.send_document(message.chat.id, doc_es, caption = 'Структура компании ГПН НС', parse_mode="html")

    # ГПН НС контакты
    elif message.text == 'Контакты ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН НС')
        doc_es = open('bot_data/presentations/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_es)
        bot.send_document(message.chat.id, doc_es, caption = 'Контакты компании ГПН НС', parse_mode="html")

    elif message.text == 'Наши корпоративные ценности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('🔙 вернуться в раздел О компании')
        doc_include = open('bot_data/presentations/corp_cen.pptx', 'rb')
        markup.add(back_button)
        bot.send_document(message.chat.id, doc_include, caption = 'Корпоративные ценности', parse_mode="html")

    elif message.text == 'Новостная лента':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('Корпоративный портал')
        btn_do_3 = types.KeyboardButton('Мобильная лента')
        btn_do_4 = types.KeyboardButton('Телеграм-каналы')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        bot.send_message(message.from_user.id, "⬇ Новостная лента", reply_markup=markup)

    elif message.text == 'Корпоративный портал':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Откройте сайт", url="https://www.gazprom-neft.ru/"))
        bot.send_message(message.chat.id, 'Корпоративный портал', reply_markup=markup)

    elif message.text == 'Мобильная лента':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_do_1 = types.InlineKeyboardButton('КАНАЛ «ГАЗПРОМ НЕФТИ»', url="HTTPS://LENTA.GAZPROM-NEFT.RU/")
        btn_do_2 = types.InlineKeyboardButton('КАНАЛ «НЕФТЕСЕРВИСЫ»', url="https://lenta.gazprom-neft.ru/channel/nefteservisy/")
        markup.add(btn_do_1, btn_do_2)
        bot.send_message(message.chat.id, 
                         'Мобильная лента:\n'
                         '\n'
                         '1. КАНАЛ «ГАЗПРОМ НЕФТИ» Главные новости компании емко и без лишних деталей, '
                         'конкурсы, тесты, прямые трансляции с мероприятий, каналы коллег о работе, '
                         'корпоративной культуре, финансах, спорте и жизни.\n'
                         '\n'
                         '2. КАНАЛ «НЕФТЕСЕРВИСЫ» Канал для блока нефтесервисов: '
                         'ГПН-НС, ГПН ЭС и ННГГФ со всеми видами активностей: '
                         'опросы, конкурсы, публикация новостей, комментарии участников.', 
                         reply_markup=markup)

    elif message.text == 'Телеграм-каналы':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_do_1 = types.InlineKeyboardButton('КОМАНДА ГПН-НС', url="https://t.me/joinchat/H_lqoksubQl5qPKFDobwMg")
        btn_do_2 = types.InlineKeyboardButton('КУЛЬТУРА И СПОРТ БРД', url="HTTPS://T.ME/SPORTCULTUREBRDHR")
        btn_do_3 = types.InlineKeyboardButton('Новости нефтесервисов', url="https://t.me/+LmDKSVvewR0yMzEy")
        btn_do_4 = types.InlineKeyboardButton('Совет молодых специалистов ЭС»', url="https://t.me/joinchat/Ez0rmolXqAS3Nzjp")
        markup.add(btn_do_1, btn_do_2, btn_do_3, btn_do_4)
        bot.send_message(message.chat.id, 
                         'Телеграм-каналы:\n'
                         '\n'
                         '1. «КОМАНДА ГПН-НС» Открытое общение сотрудников нефтесервисных предприятий\n'
                         '\n'
                         '2. «КУЛЬТУРА И СПОРТ БРД» Оперативная, актуальная и эксклюзивная информация про культуру, спорт и не только!\n'
                         '\n'
                         '3. «Новости нефтесервисов» Новости из жизни нефтесервисов\n'
                         '\n'
                         '4. «Совет молодых специалистов ЭС» Актуальная информация о деятельности Совета молодых специалистов\n', 
                         reply_markup=markup)

    elif message.text == 'Сервисы для сотрудников' or message.text == '🔙 вернуться в раздел Сервисы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('Сервисы самообслуживания')
        btn_do_3 = types.KeyboardButton('Контакт центр')
        btn_do_4 = types.KeyboardButton('Краткий справочник')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        bot.send_message(message.from_user.id, "⬇ Сервисы для сотрудников", reply_markup=markup)

    elif message.text == 'Сервисы самообслуживания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('bot_data/presentations/portal_samoobsl.pptx', 'rb')
        markup.add(btn)
        bot.send_document(message.chat.id, doc, caption = 'Сервисы самообслуживания', parse_mode="html")

    elif message.text == 'Контакт центр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('bot_data/presentations/contacts_centr.pptx', 'rb')
        markup.add(btn)
        bot.send_document(message.chat.id, doc, caption = 'Контакт центр', parse_mode="html")

    elif message.text == 'Краткий справочник':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('bot_data/presentations/404.pptx', 'rb')
        markup.add(btn)
        bot.send_document(message.chat.id, doc, caption = 'Краткий справочник', parse_mode="html")






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


if __name__ == '__main__':
    ...
