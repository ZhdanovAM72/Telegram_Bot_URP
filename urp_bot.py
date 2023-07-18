import logging
import os
import sqlite3
import datetime as dt
from logging.handlers import RotatingFileHandler

import telebot
# from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from telebot import types

from password_generator import generate_code
from db_users import get_new_user, get_new_code
from delete_utils import delete_code, delete_user
from excel import excel_export

load_dotenv()

LOG_FILE = 'bot_log.txt'  # Имя файла логов
API_TOKEN = os.getenv('URP_BOT_TOKEN')
STOP_COMMAND = os.getenv('STOP_COMMAND')
bot = telebot.TeleBot(API_TOKEN)


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


def get_admin_access(user_id: int) -> str:
    """"Проверяем данные администратора в БД."""
    with sqlite3.connect('users_v2.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT auth_code, user_id
            FROM bot_users
            WHERE user_id=? AND auth_code LIKE 'admin%'
            """,
            (user_id,)
        )
        admin_check = cursor.fetchone()
        cursor.close()
        logger.info(
            f'проверка прав администратора - '
            f'id пользователя: {user_id} - '
        )
        return admin_check


@bot.message_handler(commands=['admin'])
def check_admin_permissions(message: telebot.types.Message):
    """"Проверяем права администратора."""
    bot.send_message(message.chat.id, 'Проверяем права.')
    access = get_admin_access(message.chat.id)
    if access[1] == message.chat.id:
        bot.send_message(message.chat.id, 'Привет Admin!')
        bot.send_message(
            message.chat.id,
            'Для Вас доступны следующие команды:\n'
            '1. Создание уникального ключа доступа (/create-code).\n'
            '/create-code\n'
            '2. Выгрузка лог-файлов (/log).\n'
            '/log'
        )
    else:
        bot.send_message(message.chat.id, 'У Вас нет административных прав!')
    logger.info(
        f'команда: "admin" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'данные в БД {access[1]} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['deleteuser'])
def delete_user_from_db(message):
    """Удаляем запись из БД по user_id."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите запрос как показано на примере!\n'
        'Пример: \n/deleteuser 111111111'
    )
    if input_code == '/deleteuser':
        logger.info(
            f'команда: "{message.text}" - '
            f'пользователь: {message.from_user.username} - '
            f'id пользователя: {message.chat.id} - '
            f'имя: {message.from_user.first_name} - '
            f'фамилия: {message.from_user.last_name}'
        )
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    delete_user_id = input_code.split()
    if len(delete_user_id) <= 1 or len(delete_user_id) > 2:
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    check = search_user_id_in_db(delete_user_id[1])
    if check is not None and check[0] == int(delete_user_id[1]):
        bot.send_message(message.chat.id, 'Код найден в базе!')
        delete_user(delete_user_id[1])
        return bot.send_message(message.chat.id, 'Запись БД удалена!')
    bot.send_message(
        message.chat.id,
        'Пользователь не найден в системе!\n'
        'Проверьте user_id в БД. '
    )
    return logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['deletecode'])
def delete_code_from_db(message):
    """Удаляем запись из БД по коду доступа."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите запрос как показано на примере!\n'
        'Пример: \n/deletecode jifads9af8@!1'
    )
    if input_code == '/deletecode':
        logger.info(
            f'команда: "{message.text}" - '
            f'пользователь: {message.from_user.username} - '
            f'id пользователя: {message.chat.id} - '
            f'имя: {message.from_user.first_name} - '
            f'фамилия: {message.from_user.last_name}'
        )
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    clear_code = input_code.split()
    if len(clear_code) <= 1 or len(clear_code) > 2:
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    check = search_code_in_db(clear_code[1])
    if check is not None and check[0] == clear_code[1]:
        bot.send_message(message.chat.id, 'Код найден в базе!')
        delete_code(clear_code[1])
        return bot.send_message(message.chat.id, 'Запись БД удалена!')
    bot.send_message(
        message.chat.id,
        'Код не найден в системе!\n'
        'Проверьте код в БД. '
    )
    return logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['dbinfo'])
def export_db(message: telebot.types.Message):
    """Экспортируем БД."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')

    bot.send_message(message.chat.id, 'Попытка экспорта БД.')
    excel_export()
    export_doc_1 = open('result.xlsx', 'rb')
    export_doc_2 = open('bot_log.txt', 'rb')
    export_doc_3 = open('users_v2.sqlite', 'rb')
    date_info = dt.datetime.utcfromtimestamp(message.date)
    bot.send_document(
            message.chat.id,
            export_doc_1,
            caption=f'Выгрузка БД на {date_info.date()}',
            parse_mode="html"
            )
    bot.send_document(
            message.chat.id,
            export_doc_2,
            caption=f'Логи на {date_info.date()}',
            parse_mode="html"
            )
    bot.send_document(
            message.chat.id,
            export_doc_3,
            caption=f'Файл БД {date_info.date()}',
            parse_mode="html"
            )
    return logger.info(
        f'команда: "dbinfo" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['createcode'])
def create_new_code(message: telebot.types.Message):
    """Создаем новый код доступа в БД."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')

    bot.send_message(message.chat.id, 'Пытаемся создать новый код.')
    generate__new_code = generate_code()
    check = search_code_in_db(generate__new_code)
    if check is not None and check[0] == generate__new_code:
        bot.send_message(
            message.chat.id,
            'Данный код уже существует, '
            'повторите команду.'
        )
    elif check is None:
        bot.send_message(message.chat.id, 'Создаем новый.')
        bot.send_message(message.chat.id, 'Записываем код в БД.')
        get_new_code(generate__new_code)
        bot.send_message(message.chat.id,
                         'Код сохранен и доступен для регистрации:')
        bot.send_message(message.chat.id, generate__new_code)
    else:
        bot.send_message(message.chat.id, 'Непредвиденная ошибка.')

    return logger.info(
        f'команда: "createcode" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


def get_user_access(user_id):
    """Проверяем пользователя в БД."""
    with sqlite3.connect('users_v2.sqlite') as conn:
        cursor = conn.cursor()
        user_check_in_db = 'SELECT id, user_id FROM bot_users WHERE user_id=?'
        cursor.execute(user_check_in_db, (user_id,))
        user_check = cursor.fetchone()
        cursor.close()
        return user_check


@bot.message_handler(commands=['start'])
def check_user_permissions(message: telebot.types.Message):
    """"Определяем права пользователя."""
    access = get_user_access(message.chat.id)
    if access is None:
        bot.send_message(message.chat.id, 'Вы не зарегистрированны в системе!')
        bot.send_message(
            message.chat.id,
            'Запросите код у администратора проекта, '
            'либо используйте имеющийся.'
        )
        bot.send_message(
            message.chat.id,
            'Чтобы зарегистрироваться введите актуальный код доступа'
            ' через пробел после команды "/code"'
        )
        bot.send_message(
            message.chat.id,
            'пример кода:\n/code #your-code-1\n(Внимание код одноразовый!)'
        )
    elif access[1] == message.chat.id:
        start(message)
    else:
        bot.send_message(message.chat.id, 'Непредвиденная ошибка.')


def search_user_id_in_db(chat_id):
    """Проверяем наличие user_id в БД."""
    with sqlite3.connect('users_v2.sqlite') as conn:
        cursor = conn.cursor()
        search_db_user = ('SELECT user_id, auth_code '
                          'FROM bot_users WHERE user_id=?')
        cursor.execute(
            search_db_user,
            (chat_id,)
        )
        search_user = cursor.fetchone()
        print(search_user)
        cursor.close()
        return search_user


def search_code_in_db(code):
    """Проверяем наличие кода доступа в БД."""
    with sqlite3.connect('users_v2.sqlite') as conn:
        cursor = conn.cursor()
        search_db = ('SELECT auth_code, user_id '
                     'FROM bot_users WHERE auth_code=?')
        cursor.execute(
            search_db,
            (code,)
        )
        search_code = cursor.fetchone()
        cursor.close()
        return search_code


@bot.message_handler(commands=['code'])
def login_user(message):
    """"Определяем права пользователя."""
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите код как показано на примере!\n'
        'Пример: \n/code jifads9af8@!1'
    )
    if input_code == '/code':
        logger.info(
            f'команда: "{message.text}" - '
            f'пользователь: {message.from_user.username} - '
            f'id пользователя: {message.chat.id} - '
            f'имя: {message.from_user.first_name} - '
            f'фамилия: {message.from_user.last_name}'
        )
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    clear_code = input_code.split()
    if len(clear_code) <= 1 or len(clear_code) > 2:
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    check = search_code_in_db(clear_code[1])
    if check is not None and check[0] == clear_code[1]:
        bot.send_message(message.chat.id, 'Код найден в базе!')
        bot.send_message(message.chat.id,
                         'Проверяю возможность создания нового пользователя.')
        get_new_user(
            clear_code[1],
            message.from_user.username,
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name
        )
        return check_user_permissions(message)
    bot.send_message(
        message.chat.id,
        'Код не найден в системе!\n'
        'Запросите код у администратора проекта, '
        'либо используйте имеющийся.'
    )
    return logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=['dev_test_command'])
def start(message):
    """Приветствуем пользователя и включаем меню бота."""
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')
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
        user_info = (f'{message.from_user.username}')

    if (message.from_user.first_name is None and
       message.from_user.username is None):
        user_info = ('сотрудник')

    if (message.from_user.username is None and
       message.from_user.last_name is None):
        user_info = (f'{message.from_user.first_name}')

    start_message = (f'Привет, <b>{user_info}</b>! '
                     'Я расскажу тебе о нефтесервисных активах! '
                     'выберите интересующую вас тему в меню.')
    bot.send_message(message.chat.id,
                     start_message, parse_mode='html',
                     reply_markup=markup)
    return logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(commands=[STOP_COMMAND])  # Усложнить команду
def stop_command(message):
    """Останавливаем работу бота командой."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    bot.send_message(message.chat.id, 'OK, stop...')
    logger.critical(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    return bot.stop_polling()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    Главное меню чат-бота с глубокой вложенностью
    и возможностью возврата к предыдущему пункту меню.
    """
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')
    if message.text == 'Главное меню' or message.text == '🔙 Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('О компании')
        btn2 = types.KeyboardButton('Адаптация')
        btn3 = types.KeyboardButton('Карьерное развитие')
        btn4 = types.KeyboardButton('Цикл управления талантами')
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        # btn_do_2 = types.KeyboardButton('ГПН НС')
        btn_do_3 = types.KeyboardButton('ГПН ЭС')
        # btn_do_4 = types.KeyboardButton('ННГГФ')
        # markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_1)
        markup.add(btn_do_3, btn_do_1)
        bot.send_message(
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
        bot.send_message(
            message.from_user.id,
            "⬇ ГПН ЭС",
            reply_markup=markup
            )

    # ГПН ЭС история
    elif message.text == 'История ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('prod_data/о_компании/выбрать_ДО/ГПН_ЭС/история/о_нас.pptx', 'rb')
        markup.add(btn_history_es)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
            )

    # ГПН ЭС структура
    elif message.text == 'Структура ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton('🔙 вернуться в раздел ГПН ЭС')
        doc_es = open('prod_data/о_компании/выбрать_ДО/ГПН_ЭС/Структура/организационная_структура_ЭС.pptx', 'rb')
        markup.add(btn_structure_es)
        bot.send_document(
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
        bot.send_document(
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
        bot.send_message(message.from_user.id, "⬇ ННГГФ", reply_markup=markup)

    # ННГГФ история
    elif message.text == 'История ННГГФ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton('🔙 вернуться в раздел ННГГФ')
        doc_es = open('data/404.pptx', 'rb')  # Заплатка
        markup.add(btn_history_es)
        bot.send_document(
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
        bot.send_document(
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
        bot.send_document(
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
        bot.send_message(
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
        bot.send_document(
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
        bot.send_document(
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
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты компании ГПН НС',
            parse_mode="html"
            )

    elif message.text == 'Наши корпоративные ценности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('🔙 вернуться в раздел О компании')
        doc_include = open('prod_data/о_компании/корпоративные_ценности/корпоративные_ценности.pptx', 'rb')
        markup.add(back_button)
        bot.send_document(
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
        bot.send_message(
            message.from_user.id,
            "⬇ Новостная лента",
            reply_markup=markup
            )

    elif message.text == 'Корпоративный портал':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "«Газпром нефть»",
            url="https://www.gazprom-neft.ru/"
        ))
        bot.send_message(
            message.chat.id,
            'Корпоративный портал',
            reply_markup=markup
            )

    elif message.text == 'Мобильная лента':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_do_1 = types.InlineKeyboardButton(
            'КАНАЛ «ГАЗПРОМ НЕФТИ»',
            url="HTTPS://LENTA.GAZPROM-NEFT.RU/")
        btn_do_2 = types.InlineKeyboardButton(
            'КАНАЛ «НЕФТЕСЕРВИСЫ»',
            url="https://lenta.gazprom-neft.ru/channel/nefteservisy/")
        markup.add(btn_do_1, btn_do_2)
        bot.send_message(
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
        # Заплатка
        btn_do_1 = types.InlineKeyboardButton(
            'КОМАНДА ГПН-НС',
            url="https://t.me/+LmDKSVvewR0yMzEy"
        )
        btn_do_2 = types.InlineKeyboardButton(
            'КУЛЬТУРА И СПОРТ БРД',
            url="HTTPS://T.ME/SPORTCULTUREBRDHR"
        )
        btn_do_3 = types.InlineKeyboardButton(
            'Новости нефтесервисов',
            url="https://t.me/+LmDKSVvewR0yMzEy"
        )
        btn_do_4 = types.InlineKeyboardButton(
            'Совет молодых специалистов ЭС»',
            url="https://t.me/joinchat/Ez0rmolXqAS3Nzjp"
        )
        markup.add(btn_do_1, btn_do_2, btn_do_3, btn_do_4)
        bot.send_message(
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
        bot.send_message(
            message.from_user.id,
            "⬇ Сервисы для сотрудников",
            reply_markup=markup
            )

    elif message.text == 'Сервисы самообслуживания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('prod_data/о_компании/сервисы_для_сотрудников/портал_самообслуживания/техническая_поддержка.pptx', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Сервисы самообслуживания',
            parse_mode="html"
            )

    elif message.text == 'Контакт центр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open('prod_data/о_компании/сервисы_для_сотрудников/контакт_центр/кадровое_администрирование.pptx', 'rb')
        markup.add(btn)
        bot.send_document(
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
        bot.send_document(
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
        btn_8 = types.KeyboardButton('Буклеты для сотрудников.')
        btn_9 = types.KeyboardButton('Книги для сотрудников.')
        markup.add(
            btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_7,
            btn_8,
            btn_9,
            btn_1,
            )
        bot.send_message(
            message.from_user.id,
            "Адаптация",
            reply_markup=markup
            )

    elif message.text == 'Корпоративная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open('prod_data/Адаптация/корпоративная_безопасность/корпоративная_безопасность.pdf', 'rb')
        doc_2 = open('prod_data/Адаптация/корпоративная_безопасность/памятка_по_информационной_безопасности.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Корпоративная безопасность',
            parse_mode="html"
            )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Памятка по информационной безопасности',
            parse_mode="html"
            )

    elif message.text == 'Производственная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/производственная_безопасность/производственная_безопасность.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Производственная безопасность',
            parse_mode="html"
            )

    elif message.text == 'Хоз. и транспорт. обеспечение':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/Хозяйственное_и_транспортное_обеспечение/хозяйственное_и_транспортное_обеспечение.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Хозяйственное и транспортное обеспечение',
            parse_mode="html"
            )

    elif message.text == 'Трудовой распорядок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/Трудовой_распорядок/трудовой_распорядок.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Трудовой распорядок',
            parse_mode="html"
            )

    elif message.text == 'Внешний вид. Спецодежда и СИЗ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/внешний_вид_cпецодежда_СИЗ/внешний_вид.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Внешний вид. Спецодежда и СИЗ',
            parse_mode="html"
            )

    elif message.text == 'Мотивация персонала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/мотивация_персонала/мотивация_персонала.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Мотивация персонала',
            parse_mode="html"
            )

    elif message.text == 'Буклеты для сотрудников.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open('prod_data/Адаптация/буклеты_для_сотрудников/Буклет_сотрудника_ЭС_2023.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Буклет сотрудника.',
            parse_mode="html"
            )

    elif message.text == 'Книги для сотрудников.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open('prod_data/Адаптация/книги_для_новых_сотрудников/книга_новичка_ЭС_2023.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Книга новичка.',
            parse_mode="html"
            )

    elif (message.text == 'ДМС и РВЛ'
          or message.text == '🔙 вернуться в раздел ДМС и РВЛ'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('ДМС ЭС')
        btn_3 = types.KeyboardButton('РВЛ ЭС')
        markup.add(
            btn_2,
            btn_3,
            btn_1,
        )
        bot.send_message(
            message.from_user.id,
            "ДМС и РВЛ",
            reply_markup=markup
        )

    elif message.text == 'ДМС ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/ДМС/ГПН_ЭС/ДМС/памятка_ДМС_2023.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='ДМС в Газпромнефть Энергосистемы',
            parse_mode="html"
            )

    elif message.text == 'РВЛ ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/ДМС/ГПН_ЭС/РВЛ/памятка_санатории.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='РВЛ в Газпромнефть Энергосистемы',
            parse_mode="html"
            )

    #
    elif (message.text == 'Карьерное развитие'
          or message.text == '🔙 вернуться в раздел Карьерное развитие'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Мой трек')
        btn_3 = types.KeyboardButton('Мой профиль')
        btn_4 = types.KeyboardButton('Индивидуальный план развития')
        btn_5 = types.KeyboardButton('Карьерное консультирование')
        markup.add(
            btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_1,
        )
        bot.send_message(
            message.from_user.id,
            "Карьерное развитие",
            reply_markup=markup
        )

    elif message.text == 'Мой трек':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/карьерное_развитие/1_Мой_трек_и_карьерные_опции/Мой_трек.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Мой трек и карьерные опции',
            parse_mode="html"
            )

    elif message.text == 'Мой профиль':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc_1 = open('prod_data/карьерное_развитие/2_Профиль_на_Карьерном_Портале/Памятка_по_заполнению_профиля.pdf', 'rb')
        doc_2 = open('prod_data/карьерное_развитие/2_Профиль_на_Карьерном_Портале/Профиль_сотрудника.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Памятка по заполнению профиля',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Профиль сотрудника',
            parse_mode="html"
        )

    elif message.text == 'Индивидуальный план развития':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc_1 = open('prod_data/карьерное_развитие/3_Индивидуальный_план_развития/Актуализация_ИПР_Инструкция_для_сотрудников.pdf', 'rb')
        doc_2 = open('prod_data/карьерное_развитие/3_Индивидуальный_план_развития/ИПР_памятка_для_сотрудника.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Актуализация ИПР - Инструкция для сотрудников',
            parse_mode="html"
            )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Индивидуальный план развития - памятка для сотрудника',
            parse_mode="html"
            )

    elif message.text == 'Карьерное консультирование':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/карьерное_развитие/4_Карьерное_консультирование/Карьерное_консультирование.png', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Карьерное консультирование',
            parse_mode="html"
            )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif (message.text == 'Цикл управления талантами'
          or message.text == '🔙 вернуться в раздел Цикл управления талантами'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        # btn_2 = types.KeyboardButton('Диалоги о развитии')
        btn_3 = types.KeyboardButton('Регулярная оценка')
        btn_4 = types.KeyboardButton('Диалоги об эффективности')
        btn_5 = types.KeyboardButton('Кадровый резерв')
        btn_6 = types.KeyboardButton('Диалоги о развитии')
        # video = open('data/regular_evaluation/promo.mp4', 'rb')
        markup.add(
            # btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_1,
        )
        # bot.send_video(
        #     message.chat.id,
        #     video,
        #     caption='Оценка вклада, компетенций и ценностей',
        #     parse_mode="html",
        #     reply_markup=markup
        # )
        # Второй вариант реализации
        bot.send_message(
            message.from_user.id,
            "Цикл управления талантами",
            reply_markup=markup
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Регулярная оценка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Цикл управления талантами')
        doc_1 = open('prod_data/Цикл_управления_талантами/1_Регулярная оценка/Комиссия_по_оценке_вклада_для_сотрудников.pdf', 'rb')
        doc_2 = open('prod_data/Цикл_управления_талантами/1_Регулярная оценка/Процедуры_ежегодной_оценки_в_ГПН.pdf', 'rb')
        doc_3 = open('prod_data/Цикл_управления_талантами/1_Регулярная оценка/Регулярная_оценка_для_сотрудников.pdf', 'rb')
        doc_4 = open('prod_data/Цикл_управления_талантами/1_Регулярная оценка/Регулярная_оценка_инструкция_по_работе_с_порталом.pdf', 'rb')
        markup.add(
            types.InlineKeyboardButton(
                "Ссылка на курс",
                url=("https://edu.gazprom-neft.ru/view_doc.html?"
                     "mode=course&object_id=7060403380104215139")
            )
        )
        markup.add(btn)
        bot.send_message(
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
            'и многое другое.\n'
            'Ссылка на курс:',
            reply_markup=markup,
        )
        bot.send_message(
            message.chat.id,
            "https://edu.gazprom-neft.ru/view_doc.html?mode=course&object_id=7060403380104215139",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Комиссия по оценке вклада для сотрудников',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Процедуры ежегодной оценки в ГПН',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Регулярная оценка для сотрудников',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_4,
            caption='Регулярная оценка инструкция по работе с порталом',
            parse_mode="html"
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Диалоги об эффективности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Цикл управления талантами')
        doc_1 = open(
            'prod_data/Цикл_управления_талантами/2_Диалоги об эффективности/Диалог_об_эффективности_Памятка_для_сотрудника.pdf',
            'rb'
        )
        doc_2 = open('prod_data/Цикл_управления_талантами/2_Диалоги об эффективности/Инструкция_по_чтению_отчета_регулярной_оценки.pdf',
                     'rb')
        doc_3 = open('prod_data/Цикл_управления_талантами/2_Диалоги об эффективности/ДоЭФ_2.PNG', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Диалог об эффективности - Памятка для сотрудника',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Инструкция по чтению отчета регулярной оценки 2023',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='ДоЭФ №2',
            parse_mode="html"
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Кадровый резерв':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Цикл управления талантами')
        doc_1 = open('prod_data/Цикл_управления_талантами/3_Кадровый резерв/Комитеты_по_талантам_методология.pdf', 'rb')
        doc_2 = open('prod_data/Цикл_управления_талантами/3_Кадровый резерв/Критерии_включения_в_кадровый_резерв.pdf', 'rb')
        doc_3 = open('prod_data/Цикл_управления_талантами/3_Кадровый резерв/Правила_нахождения_в_кадровом_резерве.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Комитеты по талантам методология',
            parse_mode="html"
            )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Критерии включения в кадровый резерв',
            parse_mode="html"
            )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Правила нахождения в кадровом резерве',
            parse_mode="html"
            )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Диалоги о развитии':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Цикл управления талантами')
        doc_1 = open('prod_data/Цикл_управления_талантами/4_Диалоги о развитии/Диалог_о_развитии_Методология.pdf', 'rb')
        doc_2 = open('prod_data/Цикл_управления_талантами/4_Диалоги о развитии/Меню_развивающих_действий.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Диалог о развитии - Методология',
            parse_mode="html"
            )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Меню развивающих действий',
            parse_mode="html"
            )

    # СТАЖИРОВКА
    elif (message.text == 'Стажировка' or message.text == '🔙 вернуться в '
          'раздел Стажировка'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn_1)
        doc_1 = open('prod_data/Стажировка/Бланк_плана_стажировки_сотрудника.xlsx', 'rb')
        doc_2 = open('prod_data/Стажировка/Стажировки_БРД.pdf', 'rb')
        message_text = (
            'СТАЖИРОВКА \n Позволяет работнику погрузиться '
            'в другую деятельность и получить новый опыт в короткие'
            ' сроки. \n Перед началом стажировки совместно с '
            'руководителем необходимо сформировать план на время '
            'стажировки и согласовать его с наставником '
            'принимающей стороны.\n Обязательства принимающей стороны:'
            '- Подготовка рабочего места для стажера.\n'
            '- Выполнение плана работы на время стажировки.\n'
            '- Консультирование и сопровождение стажера. \n'
            '- Экспертная помощь наставника.'
        )
        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=markup
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Стажировки БРД',
            parse_mode='html'
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Бланк плана стажировки сотрудника',
            parse_mode='html'
        )

    # ОБУЧЕНИЕ
    elif (message.text == 'Обучение' or message.text == '🔙 вернуться в '
          'раздел Обучение'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        # btn_2 = types.KeyboardButton('Обучение ГПН-Нефтесервис')
        btn_3 = types.KeyboardButton('Обучение ГПН-Энергосистемы')
        markup.add(btn_3, btn_2, btn_1)
        bot.send_message(
            message.from_user.id,
            "Раздел обучения, выбор ДО",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif (message.text == 'Обучение ГПН-Энергосистемы' or message.text == '🔙 вернуться в '
          'раздел Обучение ГПН-Энергосистемы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton('🔙 вернуться в раздел Обучение')
        btn_2 = types.KeyboardButton('Целевые образовательные программы')
        btn_3 = types.KeyboardButton('Каталог программ')
        btn_4 = types.KeyboardButton('Полезная литература')
        markup.add(btn_3, btn_2, btn_4, btn_1)
        bot.send_message(
            message.from_user.id,
            "Обучение ГПН-Энергосистемы",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Полезная литература':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение ГПН-Энергосистемы')
        doc_1 = open('prod_data/Обучение/ГПН_ЭС/Почитать/электронные_библиотеки.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Электронные библиотеки',
            parse_mode="html",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Целевые образовательные программы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение ГПН-Энергосистемы')
        doc_1 = open('prod_data/Обучение/ГПН_ЭС/Целевые_образовательные_программы/График_ЦОП_на_2023_год.xlsx', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Целевые образовательные программы график на 2023 год',
            parse_mode="html",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Каталог программ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение ГПН-Энергосистемы')
        doc_1 = open('prod_data/Обучение/ГПН_ЭС/Каталог_программ/Каталог_программ_для_сотрудников_ИТ.pdf', 'rb')
        doc_2 = open('prod_data/Обучение/ГПН_ЭС/Каталог_программ/Каталог_программ_для_сотрудников_отдела_закупок.pdf', 'rb')
        doc_3 = open('prod_data/Обучение/ГПН_ЭС/Каталог_программ/Рекомендованные_образовательные_программы.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Каталог программ для сотрудников ИТ',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Каталог программ для сотрудников отдела закупок',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Рекомендованные образовательные программы',
            parse_mode="html",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif (message.text == 'Молодежная политика'
          or message.text == '🔙 вернуться в раздел Молодежная политика'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Молодежный совет')
        # btn_3 = types.KeyboardButton('Организация практики')
        btn_4 = types.KeyboardButton('Развитие молодых специалистов')
        markup.add(btn_2, btn_4, btn_1)
        bot.send_message(
            message.from_user.id,
            "Молодежная политика",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Молодежный совет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Направления деятельности МС')
        btn_3 = types.KeyboardButton('Положение, мотивация МС')
        btn_4 = types.KeyboardButton('Структура МС')
        markup.add(btn_2, btn_3, btn_4, btn_1)
        bot.send_message(
            message.from_user.id,
            "Молодежный совет",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Направления деятельности МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Молодежный совет')
        doc = open('prod_data/Молодежная_политика/Молодежный_совет/Направления_деятельности/Направления_деятельности.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Направления деятельности МС',
            parse_mode="html",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Положение, мотивация МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Молодежный совет')
        doc_1 = open('prod_data/Молодежная_политика/Молодежный_совет/Положение_мотивация/М-14.07.04.01-06_Организация_работы_Совета_молодежи_нефтесервисных_активов.pdf', 'rb')
        doc_2 = open('prod_data/Молодежная_политика/Молодежный_совет/Положение_мотивация/Трек_вовлеченности_МС.pdf', 'rb')
        doc_3 = open('prod_data/Молодежная_политика/Молодежный_совет/Положение_мотивация/Анкета_кандидата_для_вступления_в_Совет_молодежи.docx', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Организация работы Совета молодежи',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Трек вовлеченности МС',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Анкета кандидата',
            parse_mode="html",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Структура МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Молодежный совет')
        doc = open('prod_data/Молодежная_политика/Молодежный_совет/Структура/Структура.pptx', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Структура МС',
            parse_mode="html",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Развитие молодых специалистов':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('НТК МС')
        btn_3 = types.KeyboardButton('СЛЕТ МС')
        markup.add(btn_2, btn_3, btn_1)
        bot.send_message(
            message.from_user.id,
            "Молодежный совет",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'НТК МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Молодежный совет')
        doc = open('prod_data/Молодежная_политика/Молодежный_совет/Структура/Структура.pptx', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Структура МС',
            parse_mode="html",
            reply_markup=markup,
        )

    # elif message.text == 'Обратная связь':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('Главное меню')

    else:
        message.text == 'Информация о боте'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_info_0 = types.KeyboardButton('Главное меню')
        markup.add(btn_info_0)
        bot.send_message(
            message.from_user.id,
            'Переходи в главное меню и узнай самую важную '
            'информацию о нефтесервисных активах!',
            parse_mode='html',
            reply_markup=markup,
            )
    return logger.info(
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
def get_user_photo(message):
    """Ловим отправленные пользователем изобращения."""
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        # Рефакторинг логгера добавить
        logger.info(
            f'изображение - {message.photo}'
            f'пользователь: {message.from_user.username} - '
            f'id пользователя: {message.chat.id} - '
            f'имя: {message.from_user.first_name} - '
            f'фамилия: {message.from_user.last_name}'
        )
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')

    bot.send_message(
        message.chat.id,
        'У меня нет глаз, '
        'я не понимаю что на этой картинке.\n'
        'Давай продолжим работать в меню.'
        )
    return logger.info(
        f'изображение - {message.photo}'
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


@bot.message_handler(content_types=['sticker'])
def get_user_stiсker(message):
    """Ловим отправленные пользователем стикеры."""
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        # Необходим рефакторинг логгера
        logger.info(
            f'изображение {message.photo} - '
            f'пользователь: {message.from_user.username} - '
            f'id пользователя: {message.chat.id} - '
            f'имя: {message.from_user.first_name} - '
            f'фамилия: {message.from_user.last_name}'
        )
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')
    bot.send_message(
        message.chat.id,
        'У меня нет глаз, '
        'я не вижу этот стикер.\n'
        'Давай продолжим работать в меню.'
        )
    return logger.info(
        f'стикер {message.sticker} - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
