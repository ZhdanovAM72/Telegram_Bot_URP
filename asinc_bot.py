import os
import sqlite3
from random import choice
import logging
from logging.handlers import RotatingFileHandler

import asyncio
import aiohttp
import telebot
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

LOG_FILE = 'bot_log'
API_TOKEN = os.getenv('URP_BOT_TOKEN')
# bot = telebot.TeleBot(API_TOKEN)
bot = AsyncTeleBot(API_TOKEN)


def init_logger() -> logging.Logger:
    """Определяем настройки логгера."""
    logging.basicConfig(
        format=('%(asctime)s - %(levelname)s - %(name)s - '
                'строка: %(lineno)d - %(message)s'),
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=5_000_000,
                backupCount=5
            )
        ],
    )
    return logging.getLogger(__name__)


logger = init_logger()


@bot.message_handler(commands=['start'])
async def start(message: telebot.types.Message):
    """Приветствуем пользователя."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn01 = types.KeyboardButton('Информация о боте')
    btn02 = types.KeyboardButton('Главное меню')
    markup.add(btn01, btn02)

    if (message.from_user.first_name is not None and
       message.from_user.last_name is not None):
        user_info = (f'{message.from_user.first_name} '
                     f'{message.from_user.last_name}')

    if (message.from_user.first_name is not None and
       message.from_user.last_name is None):
        user_info = (f'{message.from_user.first_name}')

    if (message.from_user.first_name is None or
       message.from_user.last_name is None):
        user_info = (f'{message.from_user.username}')

    start_message = (f'Привет, <b>{user_info}</b>! '
                     'Я расскажу тебе о нефтесервисных активах! '
                     'выберите интересующую вас тему в меню.')
    await bot.send_message(
        message.chat.id,
        start_message,
        parse_mode='html',
        reply_markup=markup
    )
    logger.info(
        f'команда: "start" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['stp'])
async def stop_command(message: telebot.types.Message):
    """Останавливаем работу бота командой."""
    bot.send_message(message.chat.id, 'OK, stop...')
    print("OK, stop...")
    logger.critical(
        f'команда: "stp" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    bot.stop_polling()


@bot.message_handler(content_types=['text'])
async def get_text_messages(message: telebot.types.Message):
    """
    Главное меню чат-бота с глубокой вложенностью
    и возможностью возврата к предыдущему пункту меню.
    """
    if message.text == 'Главное меню' or message.text == '🔙 Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('О компании')
        btn2 = types.KeyboardButton('Адаптация')
        btn3 = types.KeyboardButton('Карьерное развитие')
        btn4 = types.KeyboardButton('Оценка вклада, компетенций и ценностей')
        btn5 = types.KeyboardButton('Обучение')
        btn6 = types.KeyboardButton('Стажировка')
        btn7 = types.KeyboardButton('ДМС и РВЛ')
        btn8 = types.KeyboardButton('Молодежная политика')
        btn9 = types.KeyboardButton('Обратная связь')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        await bot.send_message(message.from_user.id,
                         "Добро пожаловать в главное меню чат-бота",
                         reply_markup=markup)
        await bot.send_message(message.from_user.id,
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
        await bot.send_message(
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
        await bot.send_message(
            message.from_user.id,
            "⬇ Выбрать ДО",
            reply_markup=markup
            )

    # ГПН ЭС
    elif (message.text == 'ГПН ЭС'
          or message.text == '🔙 вернуться в раздел ГПН ЭС'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ЭС')
        btn_es_3 = types.KeyboardButton('Структура ЭС')
        btn_es_4 = types.KeyboardButton('Контакты ЭС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        await bot.send_message(
            message.from_user.id,
            "⬇ ГПН ЭС",
            reply_markup=markup
            )

    # ГПН ЭС история
    elif message.text == 'История ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('data/about_company/history_ES.pptx', 'rb')
        markup.add(btn_history_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
            )

    # ГПН ЭС структура
    elif message.text == 'Структура ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('data/about_company/structure_ES.pptx', 'rb')
        markup.add(btn_structure_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура компании ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
            )

    # ГПН ЭС контакты
    elif message.text == 'Контакты ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты компании ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
            )

    # ННГГФ
    elif (message.text == 'ННГГФ'
          or message.text == '🔙 вернуться в раздел ННГГФ'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ННГГФ')
        btn_es_3 = types.KeyboardButton('Структура ННГГФ')
        btn_es_4 = types.KeyboardButton('Контакты ННГГФ')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        await bot.send_message(message.from_user.id, "⬇ ННГГФ", reply_markup=markup)

    # ННГГФ история
    elif message.text == 'История ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_history_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ННГГФ',
            parse_mode="html"
            )

    # ННГГФ структура
    elif message.text == 'Структура ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_nnggf = types.KeyboardButton('🔙 вернуться '
                                                   'в раздел ННГГФ')
        doc_es = open('data/about_company/structure_NNGGF.pptx', 'rb')
        markup.add(btn_structure_nnggf)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура компании ННГГФ',
            parse_mode="html"
            )

    # ННГГФ контакты
    elif message.text == 'Контакты ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты компании ННГГФ',
            parse_mode="html"
            )

    # ГПН НС
    elif (message.text == 'ГПН НС'
          or message.text == '🔙 вернуться в раздел ГПН НС'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История ГПН НС')
        btn_es_3 = types.KeyboardButton('Структура ГПН НС')
        btn_es_4 = types.KeyboardButton('Контакты ГПН НС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        await bot.send_message(
            message.from_user.id,
            "⬇ ГПН НС",
            reply_markup=markup
            )

    # ГПН НС история
    elif message.text == 'История ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_ns = types.KeyboardButton('🔙 вернуться в раздел ГПН НС')
        doc_ns = open('data/about_company/history_NS.pptx', 'rb')
        markup.add(btn_history_ns)
        await bot.send_document(
            message.chat.id,
            doc_ns,
            caption='История ГПН НС',
            parse_mode="html"
            )

    # ГПН НС структура
    elif message.text == 'Структура ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_nnggf = types.KeyboardButton('🔙 вернуться в '
                                                   'раздел ГПН НС')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_nnggf)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура компании ГПН НС',
            parse_mode="html"
            )

    # ГПН НС контакты
    elif message.text == 'Контакты ГПН НС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН НС')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_structure_es)
        await bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты компании ГПН НС',
            parse_mode="html"
            )

    elif message.text == 'Наши корпоративные ценности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('🔙 вернуться в раздел О компании')
        doc_include = open('data/about_company/corporate_values.pptx', 'rb')
        markup.add(back_button)
        await bot.send_document(
            message.chat.id,
            doc_include,
            caption='Корпоративные ценности',
            parse_mode="html"
            )

    elif message.text == 'Новостная лента':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('Корпоративный портал')
        btn_do_3 = types.KeyboardButton('Мобильная лента')
        btn_do_4 = types.KeyboardButton('Телеграм-каналы')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        await bot.send_message(
            message.from_user.id,
            "⬇ Новостная лента",
            reply_markup=markup
            )

    elif message.text == 'Корпоративный портал':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("«Газпром нефть»", url="https://www.gazprom-neft.ru/"))
        await bot.send_message(
            message.chat.id,
            'Корпоративный портал',
            reply_markup=markup
            )

    elif message.text == 'Мобильная лента':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_do_1 = types.InlineKeyboardButton('КАНАЛ «ГАЗПРОМ НЕФТИ»', url="HTTPS://LENTA.GAZPROM-NEFT.RU/")
        btn_do_2 = types.InlineKeyboardButton('КАНАЛ «НЕФТЕСЕРВИСЫ»', url="https://lenta.gazprom-neft.ru/channel/nefteservisy/")
        markup.add(btn_do_1, btn_do_2)
        await bot.send_message(
            message.chat.id,
            'Мобильная лента:\n'
            '\n'
            '1. КАНАЛ «ГАЗПРОМ НЕФТИ» Главные новости компании'
            ' емко и без лишних деталей, '
            'конкурсы, тесты, прямые трансляции с мероприятий,'
            ' каналы коллег о работе, '
            'корпоративной культуре, финансах, спорте и жизни.\n'
            '\n'
            '2. КАНАЛ «НЕФТЕСЕРВИСЫ» Канал для блока '
            'нефтесервисов: '
            'ГПН-НС, ГПН ЭС и ННГГФ со всеми видами активностей:'
            ' опросы, конкурсы, публикация новостей, '
            'комментарии участников.',
            reply_markup=markup
        )

    elif message.text == 'Телеграм-каналы':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_do_1 = types.InlineKeyboardButton('КОМАНДА ГПН-НС', url="https://t.me/+LmDKSVvewR0yMzEy")  # Заплатка
        btn_do_2 = types.InlineKeyboardButton('КУЛЬТУРА И СПОРТ БРД', url="HTTPS://T.ME/SPORTCULTUREBRDHR")
        btn_do_3 = types.InlineKeyboardButton('Новости нефтесервисов', url="https://t.me/+LmDKSVvewR0yMzEy")
        btn_do_4 = types.InlineKeyboardButton('Совет молодых специалистов ЭС»', url="https://t.me/joinchat/Ez0rmolXqAS3Nzjp")
        markup.add(btn_do_1, btn_do_2, btn_do_3, btn_do_4)
        await bot.send_message(
            message.chat.id,
            'Телеграм-каналы:\n'
            '\n'
            '1. «КОМАНДА ГПН-НС» Открытое общение '
            'сотрудников нефтесервисных предприятий\n'
            '\n'
            '2. «КУЛЬТУРА И СПОРТ БРД» Оперативная, '
            'актуальная и эксклюзивная информация '
            'про культуру, спорт и не только!\n'
            '\n'
            '3. «Новости нефтесервисов» Новости из '
            'жизни нефтесервисов\n'
            '\n'
            '4. «Совет молодых специалистов ЭС» '
            'Актуальная информация о деятельности '
            'Совета молодых специалистов\n',
            reply_markup=markup,
        )

    elif (message.text == 'Сервисы для сотрудников'
          or message.text == '🔙 вернуться в раздел Сервисы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('Сервисы самообслуживания')
        btn_do_3 = types.KeyboardButton('Контакт центр')
        btn_do_4 = types.KeyboardButton('Краткий справочник')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        await bot.send_message(
            message.from_user.id,
            "⬇ Сервисы для сотрудников",
            reply_markup=markup
            )

    elif message.text == 'Сервисы самообслуживания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('data/about_company/self-service_portal.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Сервисы самообслуживания',
            parse_mode="html"
            )

    elif message.text == 'Контакт центр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('data/about_company/contact_center.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Контакт центр',
            parse_mode="html"
            )

    elif message.text == 'Краткий справочник':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('data/404.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Краткий справочник',
            parse_mode="html"
            )

    elif (message.text == 'Адаптация'
          or message.text == '🔙 вернуться в раздел Адаптация'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Корпоративная безопасность')
        btn_3 = types.KeyboardButton('Производственная безопасность')
        btn_4 = types.KeyboardButton('Хоз. и транспорт. '
                                     'обеспечение')
        btn_5 = types.KeyboardButton('Трудовой распорядок')
        btn_6 = types.KeyboardButton('Внешний вид. Спецодежда и СИЗ')
        btn_7 = types.KeyboardButton('Мотивация персонала')
        markup.add(
            btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_7,
            btn_1,
            )
        await bot.send_message(
            message.from_user.id,
            "Адаптация",
            reply_markup=markup
            )

    elif message.text == 'Корпоративная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/corp_sec.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Корпоративная безопасность',
            parse_mode="html"
            )

    elif message.text == 'Производственная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/production_sec.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Производственная безопасность',
            parse_mode="html"
            )

    elif message.text == 'Хоз. и транспорт. обеспечение':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/household.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Хозяйственное и транспортное обеспечение',
            parse_mode="html"
            )

    elif message.text == 'Трудовой распорядок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/work_schedule.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Трудовой распорядок',
            parse_mode="html"
            )

    elif message.text == 'Внешний вид. Спецодежда и СИЗ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/appearance.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Внешний вид. Спецодежда и СИЗ',
            parse_mode="html"
            )

    elif message.text == 'Мотивация персонала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('data/adaptation/staff_motivation.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Мотивация персонала',
            parse_mode="html"
            )

    elif (message.text == 'Карьерное развитие'
          or message.text == '🔙 вернуться в раздел Карьерное развитие'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Консультирование')
        btn_3 = types.KeyboardButton('Мой профиль')
        btn_4 = types.KeyboardButton('Оценка')
        btn_5 = types.KeyboardButton('План развития')
        # btn_6 = types.KeyboardButton('Регулярная оценка')
        markup.add(
            btn_2,
            btn_3,
            btn_4,
            btn_5,
            # btn_6,
            btn_1,
        )
        await bot.send_message(
            message.from_user.id,
            "Карьерное развитие",
            reply_markup=markup
        )

    elif message.text == 'Консультирование':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('data/404.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Консультирование',
            parse_mode="html"
            )

    elif message.text == 'Мой профиль':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('data/career_counseling/my_profile.pdf', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Мой профиль',
            parse_mode="html"
        )

    elif message.text == 'Оценка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('data/404.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Оценка',
            parse_mode="html"
            )

    elif message.text == 'План развития':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('data/career_counseling/IPR.pdf', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='План развития',
            parse_mode="html"
            )

    # elif message.text == 'Регулярная оценка':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
    #     doc = open('data/404.pptx', 'rb')
    #     markup.add(btn)
    #     bot.send_document(
    #         message.chat.id,
    #         doc,
    #         caption='Регулярная оценка',
    #         parse_mode="html"
    #     )

    elif (message.text == 'Оценка вклада, компетенций и ценностей'
          or message.text == '🔙 вернуться в раздел Оценка вклада, компетенций и ценностей'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        # btn_2 = types.KeyboardButton('Диалоги о развитии')
        btn_3 = types.KeyboardButton('Диалоги об эффективности')
        btn_4 = types.KeyboardButton('На что влияет')
        btn_5 = types.KeyboardButton('Обратная связь по итогам оценки')
        btn_6 = types.KeyboardButton('Регулярная оценка')
        video = open('data/regular_evaluation/promo.mp4', 'rb')
        markup.add(
            # btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_1,
        )
        await bot.send_video(
            message.chat.id,
            video,
            caption='Оценка вклада, компетенций и ценностей',
            parse_mode="html",
            reply_markup=markup
        )
        # Второй вариант реализации
        # bot.send_message(
        #     message.from_user.id,
        #     "Оценка вклада, компетенций и ценностей",
        #     reply_markup=markup
        # )

    elif message.text == 'Регулярная оценка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Оценка вклада, компетенций и ценностей')
        # Второй вариант реализации
        # video = open('data/regular_evaluation/promo.mp4', 'rb')
        # markup.add(btn)
        # bot.send_video(
        #     message.chat.id,
        #     video,
        #     caption='Регулярная оценка',
        #     parse_mode="html",
        # )
        doc_1 = open('data/regular_evaluation/info.pdf', 'rb')
        doc_2 = open('data/regular_evaluation/procedural.pdf', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc_1,
            caption='Диалоги о развитии',
            parse_mode="html"
        )
        await bot.send_document(
            message.chat.id,
            doc_2,
            caption='Диалоги о развитии',
            parse_mode="html"
        )

    elif message.text == 'На что влияет':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Ссылка на курс", url="https://edu.gazprom-neft.ru/view_doc.html?mode=course&object_id=7060403380104215139"))
        await bot.send_message(
            message.chat.id,
            'Практики регулярного менеджмента - это инструмент, '
            'нацеленный на повышение эффективности и результативности '
            'работы, а также формирование и поддержание культурной среды, '
            'в которой достигаются стратегические цели компании.\n'
            '\nПрохождение данного курса будет полезно каждому сотруднику.\n'
            'Пройти его можно с любого личного устройства вне КСПД.\n'
            '\nКурс состоит из девяти модулей и рассказывает обо всех '
            'основных практиках: вы узнаете, как эффективно проводить '
            'совещания, давать обратную связь, делегировать задачи '
            'и многое другое.',
            reply_markup=markup,
        )

    # elif message.text == 'Диалоги о развитии':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn = types.KeyboardButton('🔙 вернуться в раздел Оценка вклада, компетенций и ценностей')
    #     doc = open('data/404.pptx', 'rb')
    #     markup.add(btn)
    #     bot.send_document(
    #         message.chat.id,
    #         doc,
    #         caption='Диалоги о развитии',
    #         parse_mode="html"
    #         )

    elif message.text == 'Диалоги об эффективности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Оценка вклада, компетенций и ценностей')
        doc_1 = open('data/regular_evaluation/efficiency/efficiency_dialogue.pdf', 'rb')
        doc_2 = open('data/regular_evaluation/efficiency/instruction.pdf', 'rb')
        doc_3 = open('data/regular_evaluation/efficiency/memo.PNG', 'rb')
        markup.add(btn)
        await bot.send_media_group(
            message.chat.id,
            [telebot.types.InputMediaDocument(doc_1),
             telebot.types.InputMediaDocument(doc_2),
             telebot.types.InputMediaDocument(doc_3)],
        )
        # await bot.send_document(
        #     message.chat.id,
        #     doc_1,
        #     caption='Диалог об эффективности - Памятка для сотрудника',
        #     parse_mode="html"
        # )
        # await bot.send_document(
        #     message.chat.id,
        #     doc_2,
        #     caption='Инструкция по чтению отчета регулярной оценки 2023',
        #     parse_mode="html"
        # )
        # await bot.send_document(
        #     message.chat.id,
        #     doc_3,
        #     caption='ДоЭФ №2',
        #     parse_mode="html"
        # )

    elif message.text == 'Обратная связь по итогам оценки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Оценка вклада, компетенций и ценностей')
        doc = open('data/404.pptx', 'rb')
        markup.add(btn)
        await bot.send_document(
            message.chat.id,
            doc,
            caption='Обратная связь по итогам оценки вклада, компетенций и ценностей',
            parse_mode="html"
            )

    # Ниже код, который еще не реализован.

    # elif message.text == 'Обучение':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')

    elif (message.text == 'Стажировка' or message.text == '🔙 вернуться в раздел Стажировка'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        # btn_2 = types.KeyboardButton('О процессе стажировок')
        # btn_3 = types.KeyboardButton('Бланк плана стажировок')
        markup.add(btn_1)
        doc = open('data/internship/internship_plan.pdf', 'rb')
        # message_text = (
        #     'СТАЖИРОВКА \n Позволяет работнику погрузиться '
        #     'в другую деятельность и получить новый опыт в короткие'
        #     ' сроки. \n Перед началом стажировки совместно с '
        #     'руководителем необходимо сформировать план на время '
        #     'стажировки и согласовать его с наставником '
        #     'принимающей стороны.\n Обязательства принимающей стороны:'
        #     '- Подготовка рабочего места для стажера.\n'
        #     '- Выполнение плана работы на время стажировки.\n'
        #     '- Консультирование и сопровождение стажера. \n'
        #     '- Экспертная помощь наставника.'
        # )
        await bot.send_message(
            message.chat.id,
            'СТАЖИРОВКА.\n'
            'в другой деятельности и получить новый опыт в предписании'
            ' стоит. \n Перед началом стажировки совместно с '
            'руководителем необходимо широкий план на время'
            'стажировки и согласование его с наставником'
            'принимающей стороны.\n Обязательства принимающей стороны:'
            'Подготовка рабочего места для стажера.\n'
            ' Выполнение плана работы на время стажировки.\n'
            ' Консультирование и сопровождение стажера. \n'
            'Экспертная помощь инструктора.',
            reply_markup=markup
        )
        await bot.send_document(
            message.chat.id,
            doc,
            caption='План стажировки',
            parse_mode='html'
        )
        # bot.send_document(
        #     message.chat.id,
        #     doc,
        #     caption='План стажировки',
        #     parse_mode='html',
        # )


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
        await bot.send_message(
            message.from_user.id,
            'Переходи в главное меню и узнай самую важную '
            'информацию о нефтесервисных активах!',
            parse_mode='html',
            reply_markup=markup,
            )
    logger.info(
        f'команда: {message.text} - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )

# сайт
# @bot.message_handler(commands=['website'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Открыть сайт",
#                url="http://gazpromneftenergysystems.ru"))
#     bot.send_message(message.chat.id, 'Откройте сайт', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
async def get_user_photo(message: telebot.types.Message):
    """Ловим отправленные пользователем изобращения."""
    await bot.send_message(
        message.chat.id,
        'У меня нет глаз, '
        'я не понимаю что на этой картинке.\n'
        'Давай продолжим работать в меню.'
        )
    logger.info(
        f'изображение - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(content_types=['sticker'])
async def get_user_stiсker(message: telebot.types.Message):
    """Ловим отправленные пользователем стикеры."""
    await bot.send_message(
        message.chat.id,
        'У меня нет глаз, '
        'я не вижу этот стикер.\n'
        'Давай продолжим работать в меню.'
        )
    logger.info(
        f'стикер - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


if __name__ == '__main__':
    asyncio.run(bot.polling(none_stop=True, interval=0))
