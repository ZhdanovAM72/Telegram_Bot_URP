import os
import sqlite3
import datetime as dt

import telebot
from dotenv import load_dotenv
from telebot import types

from db.db_users import (get_new_user, get_new_code,
                         create_new_moderator, update_user_code)
from db.delete_utils import delete_code, delete_user
from db.permissions import (
    get_admin_access,
    get_moderator_access,
    get_user_access,
)
from db.search import (search_user_id_in_db,
                       search_code_in_db, search_all_user_id)
from logger_setting.logger_bot import logger
from utils.password_generator import generate_code
from utils.excel import excel_export
from updates import UPDATE_MESSAGE

load_dotenv()

API_TOKEN = os.getenv('URP_BOT_TOKEN')
STOP_COMMAND = os.getenv('STOP_COMMAND')

bot = telebot.TeleBot(API_TOKEN)


def log_user_command(message):
    """Логгирование команд."""
    log_message = logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    logger.info(log_message)


@bot.message_handler(commands=['admin'])
def check_admin_permissions(message: telebot.types.Message):
    """"Проверяем права администратора."""
    bot.send_message(message.chat.id, 'Проверяем права.')
    access = get_admin_access(message.chat.id)
    if access is None:
        bot.send_message(message.chat.id, 'У Вас нет административных прав!')
    elif access[1] == message.chat.id:
        bot.send_message(message.chat.id, 'Привет Admin!')
        bot.send_message(
            message.chat.id,
            'Для Вас доступны следующие команды:\n'
            '1. Выгрузка, базы данных и лог-файлов.\n'
            '/dbinfo\n'
            '2. Создание уникального ключа доступа для регистрации новых '
            'сотрудников.\n'
            'Для сотрудника Энергосистем:\n'
            '/createcode_ES\n'
            'Для сотрудника Сервисных Технологий:\n'
            '/createcode_ST\n'
            'Для сотрудника Нефтесервисных Решений:\n'
            '/createcode_NR\n'
            'Для сотрудника Инженерно-технологического сервиса:\n'
            '/createcode_ITS\n'
            '3. Удаление пользователя по user_id.\n'
            '/deleteuser user_id\n'
            '4. Удаление пользователя по user_id.\n'
            '/deletecode unique_code\n'
            '5. Назначение модератора.\n'
            '/createmoderator\n'
            '6. Удаление модератора.\n'
            '/deletemoderator user_id\n'
            '7. Обновление кода в БД.\n'
            '/updatecode old_code company_name(es)\n'
            '8. Сообщение об обновлении чат-бота:\n'
            '/updates',
        )
    else:
        bot.send_message(message.chat.id, 'У Вас нет административных прав!')
    return log_user_command(message)


@bot.message_handler(commands=['updatecode'])
def updatecode(message: telebot.types.Message):
    """Обновляем код в БД."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите запрос как показано на примере!\n'
        'Пример: \n/updatecode 111111111'
    )
    if input_code == '/updatecode':
        bot.send_message(
            message.chat.id,
            erorr_code_message
        )
        return log_user_command(message)
    old_code = input_code.split()
    if len(old_code) <= 2 or len(old_code) > 3:
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    check = search_code_in_db(old_code[1])
    if check is not None and check[0] == str(old_code[1]):
        company_name = old_code[2]
        new_code = generate_code(company_name.lower())
        update_user_code(old_code[1], new_code)
        return bot.send_message(message.chat.id, 'Запись БД обновлена!')
    bot.send_message(
        message.chat.id,
        'Код не найден в системе!\n'
        'Проверьте code в БД. '
    )
    return log_user_command(message)


@bot.message_handler(commands=['createmoderator'])
def create_moderator(message: telebot.types.Message):
    """Создаем модератора."""
    bot.send_message(message.chat.id, 'Проверяем права.')
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите запрос как показано на примере!\n'
        'Пример: \n/createmoderator 111111111'
    )
    if input_code == '/createmoderator':
        bot.send_message(
            message.chat.id,
            erorr_code_message
        )
        return log_user_command(message)
    user_id = input_code.split()
    if len(user_id) <= 1 or len(user_id) > 2:
        return bot.send_message(
            message.chat.id,
            erorr_code_message
        )
    check = search_user_id_in_db(user_id[1])
    if check is not None and check[0] == int(user_id[1]):
        bot.send_message(message.chat.id, 'Пользователь найден в базе!')
        moderator_code = 'moderator-' + check[1]
        create_new_moderator(moderator_code, user_id[1])
        return bot.send_message(message.chat.id, 'Запись БД обновлена!')
    bot.send_message(
        message.chat.id,
        'Пользователь не найден в системе!\n'
        'Проверьте user_id в БД. '
    )
    return log_user_command(message)


@bot.message_handler(commands=['moderator'])
def check_moderator_permissions(message: telebot.types.Message):
    """"Проверяем права модератора."""
    bot.send_message(message.chat.id, 'Проверяем права.')
    access = get_moderator_access(message.chat.id)
    if access is None:
        bot.send_message(message.chat.id, 'У Вас нет прав модератора!')
    elif access[1] == message.chat.id:
        bot.send_message(message.chat.id, 'Привет Moderator!')
        bot.send_message(
            message.chat.id,
            'Для Вас доступны следующие команды:\n'
            '\n1. Создание уникального ключа доступа для регистрации новых '
            'сотрудников.\n'
            '\nДля сотрудника Энергосистем:\n'
            '/createnewcode_ES\n'
            '\nДля сотрудника Сервисных Технологий:\n'
            '/createnewcode_ST\n'
            '\nДля сотрудника Нефтесервисных Решений:\n'
            '/createnewcode_NR\n'
            '\nДля сотрудника Инженерно-технологического сервиса:\n'
            '/createnewcode_ITS\n',
        )
    else:
        bot.send_message(message.chat.id, 'У Вас нет прав модератора!')
    return log_user_command(message)


@bot.message_handler(commands=['deleteuser', 'deletemoderator'])
def delete_user_from_db(message: telebot.types.Message):
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
    if input_code == '/deleteuser' or input_code == '/deletemoderator':
        bot.send_message(message.chat.id, erorr_code_message)
        return log_user_command(message)

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
    return log_user_command(message)


@bot.message_handler(commands=['deletecode'])
def delete_code_from_db(message: telebot.types.Message):
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
        bot.send_message(message.chat.id, erorr_code_message)
        return log_user_command(message)
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
    return log_user_command(message)


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
    return log_user_command(message)


@bot.message_handler(
        commands=[
            'createcode_ES',
            'createcode_ST',
            'createcode_NR',
            'createcode_ITS'
        ]
    )
def create_code(message: telebot.types.Message):
    """Создаем новый код доступа в БД."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    company = message.text.split('_')
    if len(company) == 1:
        return bot.send_message(message.chat.id, 'Неверная команда.')
    company_name = company[1]
    generate__new_code = generate_code(company_name.lower())
    check = search_code_in_db(generate__new_code)
    if check is not None and check[0] == generate__new_code:
        bot.send_message(
            message.chat.id,
            'Данный код уже существует, '
            'повторите команду.'
        )
    elif check is None:
        get_new_code(generate__new_code)
        bot.send_message(message.chat.id,
                         'Код сохранен и доступен для регистрации:')
        bot.send_message(message.chat.id, f'/code {generate__new_code}')
    else:
        bot.send_message(message.chat.id, 'Непредвиденная ошибка.')

    return log_user_command(message)


@bot.message_handler(
        commands=[
            'createnewcode_ES',
            'createnewcode_ST',
            'createnewcode_NR',
            'createnewcode_ITS',
        ]
    )
def create_new_code(message: telebot.types.Message):
    """Создаем новый код доступа в БД."""
    access = get_moderator_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет прав модератора!')
    company = message.text.split('_')
    if len(company) == 1:
        return bot.send_message(message.chat.id, 'Неверная команда.')
    company_name = company[1]
    generate__new_code = generate_code(company_name.lower())
    check = search_code_in_db(generate__new_code)
    if check is not None and check[0] == generate__new_code:
        bot.send_message(
            message.chat.id,
            'Данный код уже существует, '
            'повторите команду.'
        )
    elif check is None:
        get_new_code(generate__new_code)
        bot.send_message(message.chat.id,
                         'Код сохранен и доступен для регистрации:')
        bot.send_message(message.chat.id, f'/code {generate__new_code}')
    else:
        bot.send_message(message.chat.id, 'Непредвиденная ошибка.')

    return log_user_command(message)


@bot.message_handler(commands=['start'])
def check_user_permissions(message: telebot.types.Message):
    """"Определяем права пользователя."""
    access = get_user_access(message.chat.id)
    if access is None:
        bot.send_message(message.chat.id,
                         'Вы не зарегистрированны в системе!')
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
            'пример кода:\n/code es1nngg2f^st3!nr4\n'
            '(Внимание код одноразовый!)'
        )
    elif access[1] == message.chat.id:
        start(message)
    else:
        bot.send_message(message.chat.id, 'Непредвиденная ошибка.')


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
        bot.send_message(
            message.chat.id,
            erorr_code_message
        )
        return log_user_command(message)
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
    return log_user_command(message)


@bot.message_handler(commands=['updates'])
def updates_info_message(message):
    """Рассылка информации о последних обновлениях."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    update_message = UPDATE_MESSAGE
    users = search_all_user_id()
    # Убрать срез на проде.
    for i in users[:2]:
        try:
            bot.send_message(chat_id=i[0], text=update_message)
            print(i[0])
        except Exception:
            raise bot.send_message(
                message.chat.id,
                f'ошибка отправки пользователю с id № {i[0]}'
            )
        finally:
            continue
    return log_user_command(message)


# Неказонченный функционал
@bot.message_handler(commands=['massmess'])
def message_to_all_auth_user(message):
    """Сообщение всем зарегистрированным пользователям."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    # функция для рассылки информации
    # (забирать инфу из аргумента после команды)
    return log_user_command(message)

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

    start_message = (f'Здравствуйте, <b>{user_info}</b>!\n'
                     'Я расскажу Вам о нефтесервисных активах! '
                     'выберите интересующую Вас тему в меню.')
    bot.send_message(message.chat.id,
                     start_message, parse_mode='html',
                     reply_markup=markup)
    return log_user_command(message)


@bot.message_handler(commands=[STOP_COMMAND])  # Усложнить команду
def stop_command(message):
    """Останавливаем работу бота командой."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id,
                                'У Вас нет административных прав!')
    bot.send_message(message.chat.id, 'OK, stop...')
    log_user_command(message)
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('О компании')
        btn2 = types.KeyboardButton('Адаптация')
        btn3 = types.KeyboardButton('Карьерное развитие')
        btn4 = types.KeyboardButton('Цикл управления талантами')
        # btn5 = types.KeyboardButton('Обучение')
        btn6 = types.KeyboardButton('Стажировка')
        btn7 = types.KeyboardButton('ДМС и РВЛ')
        btn8 = types.KeyboardButton('Молодежная политика')
        btn9 = types.KeyboardButton('Обратная связь')
        markup.add(
            btn1,
            btn2,
            btn3,
            btn4,
            # btn5,
            btn6,
            btn7,
            btn8,
            btn9
        )
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
        btn_about_3 = types.KeyboardButton('Корпоративные ценности')
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
        btn_do_2 = types.KeyboardButton('Нефтесервисные решения')
        btn_do_3 = types.KeyboardButton('Газпромнефть Энергосистемы')
        btn_do_4 = types.KeyboardButton('Инженерно-технологический сервис')
        btn_do_5 = types.KeyboardButton('Газпромнефть Сервисные технологии')
        markup.add(btn_do_2, btn_do_3, btn_do_4, btn_do_5, btn_do_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Выбрать ДО",
            reply_markup=markup
            )

    # Газпромнефть Сервисные технологии
    elif (message.text == 'Газпромнефть Сервисные технологии'
          or message.text == ('🔙 вернуться в раздел '
                              'Газпромнефть Сервисные технологии')):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_2 = types.KeyboardButton('Структура СТ')
        # btn_3 = types.KeyboardButton('Контакты НР')
        btn_4 = types.KeyboardButton('История СТ')
        markup.add(btn_2, btn_4, btn_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Газпромнефть Сервисные технологии",
            reply_markup=markup
            )

    # Газпромнефть Сервисные технологии
    elif message.text == 'История СТ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Газпромнефть Сервисные технологии'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/СТ/история/about_us.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Газпромнефть Сервисные технологии"',
            parse_mode="html"
            )

    # Газпромнефть Сервисные технологии
    elif message.text == 'Структура СТ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Газпромнефть Сервисные технологии'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/СТ/структура/structure.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура ООО "Газпромнефть Сервисные технологии"',
            parse_mode="html"
            )

    # Нефтесервисные решения
    elif (message.text == 'Нефтесервисные решения'
          or message.text == '🔙 вернуться в раздел Нефтесервисные решения'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        # btn_2 = types.KeyboardButton('Структура НР')
        # btn_3 = types.KeyboardButton('Контакты НР')
        btn_4 = types.KeyboardButton('История НР')
        markup.add(btn_4, btn_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Нефтесервисные решения",
            reply_markup=markup
        )

    # ННГГФ (ИТС) Контакты
    elif message.text == 'История НР':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Нефтесервисные решения'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/НР/История/about_us.pptx',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Нефтесервисные решения"',
            parse_mode="html"
        )

    # ННГГФ (ИТС)
    elif (message.text == 'Инженерно-технологический сервис'
          or message.text == ('🔙 вернуться в раздел '
                              'Инженерно-технологический сервис')):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('Структура ИТС')
        btn_es_3 = types.KeyboardButton('НМД ИТС')
        btn_es_4 = types.KeyboardButton('Контакты ИТС')
        btn_es_5 = types.KeyboardButton('История ИТС')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_5, btn_es_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Инженерно-технологический сервис",
            reply_markup=markup
        )

    # ННГГФ (ИТС) Контакты
    elif message.text == 'Контакты ИТС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Инженерно-технологический сервис'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/Контакты/info.docx',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты ООО "Инженерно-технологический сервис"',
            parse_mode="html"
        )

    # ННГГФ (ИТС) История
    elif message.text == 'История ИТС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Инженерно-технологический сервис'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/История/about_us.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Инженерно-технологический сервис"',
            parse_mode="html"
        )

    # ННГГФ (ИТС) Структура
    elif message.text == 'Структура ИТС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Инженерно-технологический сервис'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/Структура/structure.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура ООО "Инженерно-технологический сервис"',
            parse_mode="html"
        )

    # ННГГФ (ИТС) НМД ИТС
    elif message.text == 'НМД ИТС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Инженерно-технологический сервис'
        )
        doc_1 = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/8.pdf',
            'rb'
        )
        doc_2 = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/ib.pdf',
            'rb'
        )
        doc_3 = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/ptvr.pdf',
            'rb'
        )
        doc_4 = open(
            'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/vahta.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption=(
                'Пропускной и внутреобъектовый режимы '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Памятка по ИБ',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption=(
                'Правила внутреннего трудового распорядка '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_4,
            caption=(
                'Положение о вахтовом методе работы '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html"
        )

    # ГПН ЭС
    elif (message.text == 'Газпромнефть Энергосистемы'
          or message.text == ('🔙 вернуться в раздел '
                              'Газпромнефть Энергосистемы')):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_es_1 = types.KeyboardButton('🔙 вернуться в раздел Выбрать ДО')
        btn_es_2 = types.KeyboardButton('История Энергосистем')
        btn_es_3 = types.KeyboardButton('Структура Энергосистем')
        btn_es_4 = types.KeyboardButton('Контакты Энергосистем')
        markup.add(btn_es_2, btn_es_3, btn_es_4, btn_es_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Газпромнефть Энергосистемы",
            reply_markup=markup
        )

    # ГПН ЭС история
    elif message.text == 'История Энергосистем':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_history_es = types.KeyboardButton(
            '🔙 вернуться в раздел Газпромнефть Энергосистемы'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ГПН_ЭС/история/о_нас.pptx',
            'rb'
        )
        markup.add(btn_history_es)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='История ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
        )

    # ГПН ЭС структура
    elif message.text == 'Структура Энергосистем':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton(
            '🔙 вернуться в раздел Газпромнефть Энергосистемы'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ГПН_ЭС/Структура/организационная_структура_ЭС.pdf',
            'rb'
        )
        markup.add(btn_structure_es)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Структура компании ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
        )

    # ГПН ЭС контакты
    elif message.text == 'Контакты Энергосистем':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_structure_es = types.KeyboardButton(
            '🔙 вернуться в раздел Газпромнефть Энергосистемы'
        )
        doc_es = open(
            'prod_data/о_компании/выбрать_ДО/ГПН_ЭС/контакты/contacs.pdf',
            'rb'
        )
        markup.add(btn_structure_es)
        bot.send_document(
            message.chat.id,
            doc_es,
            caption='Контакты компании ООО "Газпромнефть Энергосистемы"',
            parse_mode="html"
        )

    elif message.text == 'Корпоративные ценности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('🔙 вернуться в раздел О компании')
        doc_include = open(
            'prod_data/о_компании/корпоративные_ценности/gpn_guide.pdf',
            'rb'
        )
        markup.add(back_button)
        bot.send_document(
            message.chat.id,
            doc_include,
            caption='Корпоративные ценности',
            parse_mode="html",
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
        doc_1 = open(
            'prod_data/о_компании/новостная_лента/corp_portal/guide.pdf',
            'rb'
        )
        markup.add(types.InlineKeyboardButton(
            "Открыть портал знаний",
            url="http://edu.gazprom-neft.ru"
        ))
        bot.send_message(
            message.chat.id,
            'Корпоративные ресурсы',
            reply_markup=markup
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Как через Интернет войти на Портал знаний',
            parse_mode="html",
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
            'Нефтесервисных решений, Энергосистем, ННГГФ, Сервисных'
            ' технологий со всеми видами активностей:'
            ' опросы, конкурсы, публикация новостей, '
            'комментарии участников.',
            reply_markup=markup
        )

    elif message.text == 'Телеграм-каналы':
        markup = types.InlineKeyboardMarkup(row_width=1)
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
            'Совет молодых специалистов',
            url="https://t.me/joinchat/Ez0rmolXqAS3Nzjp"
        )
        btn_do_5 = types.InlineKeyboardButton(
            'НТК',
            url="https://t.me/+TJe7-1a28tSJS-7Q"
        )
        markup.add(btn_do_1, btn_do_2, btn_do_3, btn_do_4, btn_do_5)
        bot.send_message(
            message.chat.id,
            'Телеграм-каналы:\n'
            '\n'
            '1. «Команда ГПН-НС» Открытое общение '
            'сотрудников нефтесервисных предприятий\n'
            '\n'
            '2. «Культура и спорт БРД» Оперативная, '
            'актуальная и эксклюзивная информация '
            'про культуру, спорт и не только!\n'
            '\n'
            '3. «Новости нефтесервисов» Новости из '
            'жизни нефтесервисов.\n'
            '\n'
            '4. «Совет молодых специалистов» '
            'Актуальная информация о деятельности '
            'Совета молодых специалистов.\n'
            '5. «Научно-техническая конференция» '
            'Актуальная информация о молодежной '
            'научно-технической конференции.\n',
            reply_markup=markup,
        )

    elif (message.text == 'Сервисы для сотрудников'
          or message.text == '🔙 вернуться в раздел Сервисы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_do_1 = types.KeyboardButton('🔙 вернуться в раздел О компании')
        btn_do_2 = types.KeyboardButton('Сервисы самообслуживания')
        btn_do_3 = types.KeyboardButton('Контакт центр')
        # btn_do_4 = types.KeyboardButton('Краткий справочник')
        markup.add(btn_do_2, btn_do_3, btn_do_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Сервисы для сотрудников",
            reply_markup=markup
        )

    elif message.text == 'Сервисы самообслуживания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Сервисы')
        doc = open(
            'prod_data/о_компании/сервисы_для_сотрудников/портал_самообслуживания/техническая_поддержка.pdf',
            'rb'
        )
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
        doc = open(
            'prod_data/о_компании/сервисы_для_сотрудников/контакт_центр/кадровое_администрирование.pptx',
            'rb'
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Контакт центр',
            parse_mode="html"
        )

    # АДАПТАЦИЯ
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
            btn_8,
            btn_9,
            btn_2,
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_7,
            btn_1,
            )
        bot.send_message(
            message.from_user.id,
            "Адаптация",
            reply_markup=markup
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Корпоративная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open(
            'prod_data/Адаптация/корпоративная_безопасность/ES.pdf',
            'rb'
        )
        doc_2 = open(
            'prod_data/Адаптация/корпоративная_безопасность/памятка.pdf',
            'rb'
        )
        doc_3 = open(
            'prod_data/Адаптация/корпоративная_безопасность/ITS.pdf',
            'rb'
        )
        doc_4 = open(
            'prod_data/Адаптация/корпоративная_безопасность/ST.pdf',
            'rb'
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Памятка по информационной безопасности',
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            protect_content=True,
            caption=(
                'Корпоративная безопасность '
                'ООО "Газпромнефть Энергосистемы"'
            ),
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            protect_content=True,
            caption=(
                'Корпоративная безопасность '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html"
        )
        bot.send_document(
            message.chat.id,
            doc_4,
            protect_content=True,
            caption='Корпоративная безопасность ООО "Сервисные технологии"',
            parse_mode="html"
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Производственная безопасность':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        document_1 = open(
            'prod_data/Адаптация/производственная_безопасность/ES_pb.pdf',
            'rb'
        )
        document_2 = open(
            'prod_data/Адаптация/производственная_безопасность/ITS_pb.pdf',
            'rb'
        )
        document_3 = open(
            'prod_data/Адаптация/производственная_безопасность/ST_NR_pb.pdf',
            'rb'
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            document_1,
            caption=(
                'Производственная безопасность '
                'ООО "Газпромнефть Энергосистемы"'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_2,
            caption=(
                'Производственная безопасность '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_3,
            caption=(
                'Производственная безопасность '
                'ООО "Нефтесервисные решения" и '
                'ООО "Газпромнефть Сервисные технологии"'
            ),
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Хоз. и транспорт. обеспечение':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        document_1 = open('prod_data/Адаптация/hoz_trans/ES.pdf', 'rb')
        document_2 = open('prod_data/Адаптация/hoz_trans/ITS.pdf', 'rb')
        document_3 = open('prod_data/Адаптация/hoz_trans/NR.pdf', 'rb')
        markup.add(button)
        bot.send_document(
            message.chat.id,
            document_1,
            caption=(
                'Хозяйственное и транспортное обеспечение '
                'ООО "Газпромнефть Энергосистемы"'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_2,
            caption=(
                'Хозяйственное и транспортное обеспечение '
                'ООО "Инженерно-технологический Сервис"'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_3,
            caption=(
                'Хозяйственное и транспортное обеспечение '
                'ООО "Нефтесервисные Решения"'
            ),
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Трудовой распорядок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        document_1 = open(
            'prod_data/Адаптация/trudovoi_raspor/es_trud.pdf',
            'rb',
        )
        document_2 = open(
            'prod_data/Адаптация/trudovoi_raspor/its_trud.pdf',
            'rb',
        )
        document_3 = open(
            'prod_data/Адаптация/trudovoi_raspor/nr_trud.pdf',
            'rb',
        )
        document_4 = open(
            'prod_data/Адаптация/trudovoi_raspor/st_trud.pdf',
            'rb',
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            document_1,
            caption='Трудовой распорядок в ООО "Газпромнефть Энергосистемы"',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_2,
            caption=(
                'Трудовой распорядок в '
                'ООО "Инженерно-технологический Сервис"'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_3,
            caption='Трудовой распорядок в ООО "Нефтесервисные Решения"',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_4,
            caption=(
                'Трудовой распорядок в '
                'ООО "Газпромнефть Сервисные технологии"'
            ),
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Внешний вид. Спецодежда и СИЗ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc = open('prod_data/Адаптация/vnesh_vid/vneshsiz.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Внешний вид. Спецодежда и СИЗ',
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Мотивация персонала':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        button_2 = types.KeyboardButton('Мотивация ЭС')
        button_3 = types.KeyboardButton('Мотивация НР')
        button_4 = types.KeyboardButton('Мотивация ИТС')
        button_5 = types.KeyboardButton('Мотивация СТ')
        markup.add(button_2, button_3, button_4, button_5, button_1)
        bot.send_message(
            message.from_user.id,
            "⬇ Мотивация персонала",
            reply_markup=markup,
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Мотивация ЭС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в Мотивация персонала')
        document = open(
            'prod_data/Адаптация/мотивация_персонала/ES_motivate.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            document,
            caption='Мотивация сотрудников ООО "Газпромнефть Энергосистемы"',
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Мотивация НР':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в Мотивация персонала')
        document = open(
            'prod_data/Адаптация/мотивация_персонала/NR_motivate.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            document,
            caption='Мотивация сотрудников ООО "Нефтесервисные решения"',
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Мотивация ИТС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в Мотивация персонала')
        document = open(
            'prod_data/Адаптация/мотивация_персонала/ITS_motivate.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            document,
            caption=(
                'Мотивация сотрудников '
                'ООО "Инженерно-технологический сервис"'
            ),
            parse_mode="html"
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Мотивация СТ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в Мотивация персонала')
        document = open(
            'prod_data/Адаптация/мотивация_персонала/ST_motivate.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            document,
            caption=(
                'Мотивация сотрудников '
                'ООО "Газпромнефть Сервисные технологии"'
            ),
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Буклеты для сотрудников.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open(
            'prod_data/Адаптация/буклеты_для_сотрудников/ES_2023.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/Адаптация/буклеты_для_сотрудников/NR_2023.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Адаптация/буклеты_для_сотрудников/ST_2023.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Буклет сотрудника ООО "Газпромнефть Энергосистемы.',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Буклет сотрудника ООО "Нефтесервисные решения.',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Буклет сотрудника ООО "Газпромнефть Сервисные технологии',
            parse_mode="html",
        )

    # АДАПТАЦИЯ =
    elif message.text == 'Книги для сотрудников.':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        doc_1 = open(
            'prod_data/Адаптация/книги_для_новых_сотрудников/ES_book.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/Адаптация/книги_для_новых_сотрудников/NR_book.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Адаптация/книги_для_новых_сотрудников/ITS_book.pdf',
            'rb',
        )
        doc_4 = open(
            'prod_data/Адаптация/книги_для_новых_сотрудников/ST_book.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption=(
                'Книга для нового сотрудника '
                'ООО "Газпромнефть Энергосистемы".'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption=(
                'Книга для нового сотрудника '
                'ООО "Нефтесервисные решения".'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption=(
                'Книга для нового сотрудника '
                'ООО "Инженерно-технологический сервис".'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_4,
            caption=(
                'Книга для нового сотрудника '
                'ООО "Газпромнефть Сервисные технологии".'
            ),
            parse_mode="html",
        )

    # ДМС и РВЛ
    elif (message.text == 'ДМС и РВЛ'
          or message.text == '🔙 вернуться в раздел ДМС и РВЛ'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('ДМС')
        btn_3 = types.KeyboardButton('РВЛ')
        doc = open('prod_data/ДМС/ГПН_ЭС/curators.pdf', 'rb')
        markup.add(
            btn_2,
            btn_3,
            btn_1,
        )
        bot.send_message(
            message.from_user.id,
            "ДМС и РВЛ",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc,
            caption='Кураторы программы в ДО и подразделениях',
            parse_mode="html",
        )

    # ДМС и РВЛ
    elif message.text == 'ДМС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc_1 = open('prod_data/ДМС/ГПН_ЭС/ДМС/памятка_ДМС_2023.pdf', 'rb')
        doc_2 = open('prod_data/ДМС/ГПН_ЭС/ДМС/med_list.pdf', 'rb')
        doc_3 = open('prod_data/ДМС/ГПН_ЭС/ДМС/dms.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Памятка по лечению',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Перечень поликлиник',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Программа ДМС',
            parse_mode="html",
        )

    # ДМС и РВЛ
    elif message.text == 'РВЛ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/ДМС/ГПН_ЭС/РВЛ/памятка_санатории.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Памятка по санаториям',
            parse_mode="html",
        )

    # КАРЬЕРНОЕ РАЗВИТИЕ
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
            reply_markup=markup,
        )

    # КАРЬЕРНОЕ РАЗВИТИЕ
    elif message.text == 'Мой трек':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/карьерное_развитие/my_track/my.pdf', 'rb')
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Мой трек и карьерные опции',
            parse_mode="html",
        )

    # КАРЬЕРНОЕ РАЗВИТИЕ
    elif message.text == 'Мой профиль':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc_1 = open(
            'prod_data/карьерное_развитие/profile_on_portal/info.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/карьерное_развитие/profile_on_portal/profile.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            'Профиль на карьерном портале -это Ваша визитная карточка, '
            'в которой отображаются ваши уникальные навыки и квалификация,'
            ' она подчеркивает преимущества, которые вы можете '
            'предложить работодателю.\n'
            '\nЗдесь собирается вся информация о Вас как о специалисте:\n'
            '- информация об образовании,\n'
            '- профессиональной квалификации,\n'
            '- соответствующем опыте работы,\n'
            '- навыках и заметных достижениях\n'
            '\nРегулярно обновляйте профиль, чтобы руководители и HR '
            'смогли видеть самую актуальную информацию о Вас.',
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Памятка по заполнению профиля',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Профиль сотрудника',
            parse_mode="html",
        )

    # КАРЬЕРНОЕ РАЗВИТИЕ
    elif message.text == 'Индивидуальный план развития':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Карьерное развитие'
        )
        document_1 = open(
            'prod_data/карьерное_развитие/individual_plan/instruction.pdf',
            'rb',
        )
        document_2 = open(
            'prod_data/карьерное_развитие/individual_plan/IPR.pdf',
            'rb',
        )
        document_3 = open(
            'prod_data/карьерное_развитие/individual_plan/menu.pdf',
            'rb',
        )
        document_4 = open(
            'prod_data/карьерное_развитие/individual_plan/plan.pdf',
            'rb',
        )
        document_5 = open(
            'prod_data/карьерное_развитие/individual_plan/done.pdf',
            'rb',
        )
        markup.add(button)
        bot.send_document(
            message.chat.id,
            document_2,
            caption='Индивидуальный план развития - памятка для сотрудника',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_4,
            caption=(
                'Формирование плана развития - '
                'Памятка для сотрудников 2023'
            ),
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_3,
            caption='Меню развивающих действий',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_1,
            caption='Актуализация ИПР - Инструкция для сотрудников',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_5,
            caption='Факт выполнения целей в ИПР',
            parse_mode="html",
            reply_markup=markup,
        )

    # КАРЬЕРНОЕ РАЗВИТИЕ
    elif message.text == 'Карьерное консультирование':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Карьерное развитие')
        doc = open('prod_data/карьерное_развитие/carier_couch/file.png', 'rb')
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            'Предмет карьерного консультирования — профессиональное и'
            'карьерное развитие сотрудника на протяжении '
            'всей его трудовой деятельности.\n'
            '\nЭто совместная деятельность карьерного консультанта '
            'и сотрудника по определению ценностей и профессиональных '
            'интересов, анализу ближайших и долгосрочных целей, '
            'ресурсов и возможностей сотрудника для достижения позитивных '
            'изменений в профессиональной деятельности.\n'
            '\nВы можете записаться на карьерную консультацию на'
            ' Карьерном портале при условии, что Ваш профиль '
            'заполнен не менее чем на 80%.',
        )
        bot.send_document(
            message.chat.id,
            doc,
            caption='Карьерное консультирование',
            parse_mode="html",
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif (message.text == 'Цикл управления талантами'
          or message.text == '🔙 вернуться в раздел Цикл управления талантами'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        btn_2 = types.KeyboardButton('Обучение')
        btn_3 = types.KeyboardButton('Регулярная оценка')
        btn_4 = types.KeyboardButton('Диалоги об эффективности')
        btn_5 = types.KeyboardButton('Комитеты по талантам')
        btn_6 = types.KeyboardButton('Диалоги о развитии')

        markup.add(
            btn_3,
            btn_4,
            btn_5,
            btn_6,
            btn_2,
            btn_1,
        )

        bot.send_message(
            message.from_user.id,
            "Цикл управления талантами",
            reply_markup=markup,
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif (message.text == 'Регулярная оценка'
          or message.text == '🔙 вернуться в раздел Регулярная оценка'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(
            '🔙 вернуться в раздел Цикл управления талантами'
        )
        btn_1 = types.KeyboardButton('Комиссия по оценке вклада')
        doc_2 = open(
            'prod_data/Цикл_управления_талантами/Регулярная_оценка/Процедуры.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Цикл_управления_талантами/Регулярная_оценка/для_сотрудников.pdf',
            'rb',
        )
        markup.add(btn_1, btn)

        bot.send_document(
            message.chat.id,
            doc_2,
            reply_markup=markup,
            caption='Процедуры ежегодной оценки в ГПН',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Регулярная оценка для сотрудников',
            parse_mode="html",
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Комиссия по оценке вклада':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Регулярная оценка')
        markup.add(btn)
        doc_1 = open(
            'prod_data/Цикл_управления_талантами/Регулярная_оценка/Комиссия.pdf',
            'rb',
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Комиссия по оценке вклада для сотрудников',
            parse_mode="html",
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Диалоги об эффективности':
        doc_2 = open(
            'prod_data/Цикл_управления_талантами/Диалоги_об_эффективности/Инструкция.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Цикл_управления_талантами/Диалоги_об_эффективности/ДоЭФ.PNG',
            'rb',
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("смотреть видео",
                   url="https://youtu.be/O2JyX9iL8Hs"))
        bot.send_message(
            message.chat.id,
            'Диалог об эффективности',
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Инструкция по чтению отчета регулярной оценки 2023',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Помятка для сотрудника',
            parse_mode="html",
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Комитеты по талантам':
        doc_1 = open(
            'prod_data/Цикл_управления_талантами/comitet/nmd.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/Цикл_управления_талантами/comitet/PR_criteria.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Цикл_управления_талантами/comitet/rules.pdf',
            'rb',
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("смотреть видео",
                   url="https://youtu.be/yxILbJcIFA8"))
        bot.send_message(
            message.chat.id,
            'Комитеты по талантам',
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Комитеты по талантам методология',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Критерии включения в кадровый резерв',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Правила нахождения в кадровом резерве',
            parse_mode="html",
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Диалоги о развитии':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(
            '🔙 вернуться в раздел Цикл управления талантами'
        )
        doc_1 = open(
            'prod_data/Цикл_управления_талантами/Диалоги_о_развитии/Методология.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/Цикл_управления_талантами/Диалоги_о_развитии/difference.pdf',
            'rb',
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("смотреть видео",
                   url="https://youtu.be/HZB4eES30XI"))
        bot.send_message(message.chat.id, 'Диалог о развитии', reply_markup=markup)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Диалог о развитии - Методология',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption=('Разница между диалогом о развитии'
                     ' и диалогом об эффективности'),
            parse_mode="html",
        )

    # СТАЖИРОВКА
    elif (message.text == 'Стажировка' or message.text == '🔙 вернуться в '
          'раздел Стажировка'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn_1)
        doc_1 = open(
            'prod_data/Стажировка/Бланк_плана_стажировки_сотрудника.xlsx',
            'rb',
        )
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
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Стажировки БРД',
            parse_mode='html',
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Бланк плана стажировки сотрудника',
            parse_mode='html',
        )

    # ОБУЧЕНИЕ
    elif (message.text == 'Обучение' or message.text == '🔙 вернуться в '
          'раздел Обучение'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button_1 = types.KeyboardButton(
            '🔙 вернуться в раздел Цикл управления талантами'
        )
        button_2 = types.KeyboardButton('Цикл планирования обучения')
        button_3 = types.KeyboardButton('Каталог программ')
        button_4 = types.KeyboardButton('Полезная литература')
        button_5 = types.KeyboardButton('Планирование обучения')
        markup.add(button_3, button_2, button_4, button_5, button_1)
        bot.send_message(
            message.from_user.id,
            "Обучение",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Планирование обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Обучение')
        document_1 = open(
            'prod_data/Обучение/ГПН_ЭС/plan/employee.pdf',
            'rb',
        )
        document_2 = open(
            'prod_data/Обучение/ГПН_ЭС/plan/supervisor.pdf',
            'rb',
        )
        markup.add(button_1)
        bot.send_document(
            message.chat.id,
            document_1,
            caption='Планирование обучения - Сотрудник',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_2,
            caption='Планирование обучения - Руководитель',
            parse_mode="html",
            reply_markup=markup,
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Полезная литература':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение')
        doc_1 = open(
            'prod_data/Обучение/ГПН_ЭС/Почитать/электронные_библиотеки.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Электронные библиотеки',
            parse_mode="html",
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Цикл планирования обучения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение')
        doc_1 = open(
            'prod_data/Обучение/ГПН_ЭС/Целевые_образовательные_программы/educate.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Цикл планирования обучения',
            parse_mode="html",
        )

    # ОБУЧЕНИЕ
    elif message.text == 'Каталог программ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Обучение')
        doc_1 = open(
            'prod_data/Обучение/ГПН_ЭС/Каталог_программ/Рекомендованные_образовательные_программы.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Рекомендованные образовательные программы',
            parse_mode="html",
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif (message.text == 'Молодежная политика'
          or message.text == '🔙 вернуться в раздел Молодежная политика'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
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
    elif (message.text == 'Молодежный совет'
          or message.text == '🔙 вернуться в '
                             'раздел Молодежный совет'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(
            '🔙 вернуться в раздел Молодежная политика'
        )
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
        doc = open(
            'prod_data/Молодежная_политика/MS/Направления_деятельности/napravlenya.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Направления деятельности МС',
            parse_mode="html",
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Положение, мотивация МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Молодежный совет')
        doc_1 = open(
            'prod_data/Молодежная_политика/MS/Положение_мотивация/workorgMS.pdf',
            'rb',
        )
        doc_2 = open(
            'prod_data/Молодежная_политика/MS/Положение_мотивация/trackMS.pdf',
            'rb',
        )
        doc_3 = open(
            'prod_data/Молодежная_политика/MS/Положение_мотивация/AnketaMS.docx',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Организация работы Совета молодежи',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Трек вовлеченности МС',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Анкета кандидата',
            parse_mode="html",
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Структура МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Молодежный совет')
        doc = open(
            'prod_data/Молодежная_политика/MS/Структура/structuraMS.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Структура МС',
            parse_mode="html",
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif (message.text == 'Развитие молодых специалистов'
          or message.text == ('🔙 вернуться в раздел '
                              'Развитие молодых специалистов')):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(
            '🔙 вернуться в раздел Молодежная политика'
        )
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
                                   'раздел Развитие молодых специалистов')
        doc_1 = open(
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/НТК/Заявка_Шаблон.docx',
            'rb',
        )
        doc_2 = open(
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/НТК/Шаблон_одностраничника.pptx',
            'rb',
        )
        doc_3 = open(
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/НТК/Шаблон_презентации.pptx',
            'rb',
        )
        doc_4 = open(
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/НТК/dk.pdf',
            'rb',
        )
        markup.add(btn)
        bot.send_message(
            message.from_user.id,
            'Научно – техническая конференция – это мероприятие, '
            'проводящееся на ежегодной основе, с целью продвижения '
            'научного потенциала молодых специалистов и работников компании,'
            ' а также с целью обмена опытом между молодыми специалистами '
            'дочерних обществ и совместных предприятий, демонстрации '
            'инноваций, апробирования новых технологий и процессов, '
            'укрепления имиджа компании и повышения заинтересованности '
            'работников в совершенствовании профессиональных навыков.\n'
            '\nНТК проводится в 3 этапа:\n'
            'Локальная НТК\n'
            'НТК Блока разведки и добычи\n'
            'Корпоративный финал НТК \n'
            '\nПочему стоит принять участие в конференции?\n'
            '-  Возможность раскрыть потенциал и заявить о себе;\n'
            '-  Возможность повысить экспертизу в рамках направления своей '
            'деятельности;\n'
            '-  Возможность принять участие в дальнейшей реализации '
            'проектов;\n'
            '-  Возможность найти единомышленников.',
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_1,
            caption='Заявка - Шаблон',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_2,
            caption='Шаблон одностраничника',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_3,
            caption='Шаблон презентации',
            parse_mode="html",
            reply_markup=markup,
        )
        bot.send_document(
            message.chat.id,
            doc_4,
            caption='Шаблон презентации',
            parse_mode="html",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'СЛЕТ МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в '
                                   'раздел Развитие молодых специалистов')
        doc = open(
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/Слет_МС/Слет_МС.pptx',
            'rb',
        )
        markup.add(btn)
        bot.send_document(
            message.chat.id,
            doc,
            caption='Слет МС',
            parse_mode="html",
            reply_markup=markup,
        )

    elif message.text == 'Обратная связь':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Главное меню')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Заполнить форму",
                   url="https://forms.yandex.ru/u/64f4d1a4068ff09dca58ac3c/"))
        bot.send_message(message.chat.id,
                         'Форма обратной связи', reply_markup=markup)

    else:
        message.text == 'Информация о боте'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_info_0 = types.KeyboardButton('Главное меню')
        markup.add(btn_info_0)
        bot.send_message(
            message.from_user.id,
            'Переходи в главное меню и узнай самую важную '
            'информацию о нефтесервисных активах!\n'
            'Для администратора и модераторов чат-бота '
            'доступны дополнительные команды:\n'
            '/admin\n'
            '/moderator\n',
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
        'Давайте продолжим работать в меню.',
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
        'Давайте продолжим работать в меню.',
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
