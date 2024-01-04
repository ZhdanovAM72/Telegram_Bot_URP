import datetime as dt
import os

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
from logger_setting.logger_bot import log_user_command, log_photo, log_sticker
from utils.password_generator import generate_code
from utils.excel import excel_export
from updates import UPDATE_MESSAGE
from constant import (
    ES, ITS, NR, NNGGF, ST,
    ABOUT_NTK,
    ADMIN_COMMANDS,
    NO_ADMIN_RIGHTS,
    MODERATOR_COMMANDS,
    NO_MODERATOR_RIGHTS,
    MAX_MESSAGE_SYMBOLS
)

load_dotenv()

API_TOKEN = os.getenv('URP_BOT_TOKEN')
STOP_COMMAND = os.getenv('STOP_COMMAND')

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['admin'])
def check_admin_permissions(message: telebot.types.Message):
    """"Проверяем права администратора."""
    bot.send_message(message.chat.id, 'Проверяем права.')
    access = get_admin_access(message.chat.id)
    if access is None:
        bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
    elif access[1] == message.chat.id:
        bot.send_message(message.chat.id, 'Привет Admin!')
        bot.send_message(message.chat.id, text=ADMIN_COMMANDS)
    else:
        bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
    return log_user_command(message)


@bot.message_handler(commands=['updatecode'])
def updatecode(message: telebot.types.Message):
    """Обновляем код в БД."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
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
        return bot.send_message(message.chat.id, NO_ADMIN_RIGHTS)
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
        bot.send_message(message.chat.id, text=NO_MODERATOR_RIGHTS)
    elif access[1] == message.chat.id:
        bot.send_message(message.chat.id, 'Привет Moderator!')
        bot.send_message(message.chat.id, text=MODERATOR_COMMANDS)
    else:
        bot.send_message(message.chat.id, text=NO_MODERATOR_RIGHTS)
    return log_user_command(message)


@bot.message_handler(commands=['deleteuser', 'deletemoderator'])
def delete_user_from_db(message: telebot.types.Message):
    """Удаляем запись из БД по user_id."""
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
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
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
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
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)

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
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
    company = message.text.split('_')
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
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
    company = message.text.split('_')
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
    """Определяем права пользователя."""
    input_code = message.text
    erorr_code_message = (
        'Команда использована неверно, '
        'введите код как показано на примере!\n'
        'Пример: \n/code jifads9af8@!1'
    )
    if input_code == '/code':
        bot.send_message(
            message.chat.id,
            erorr_code_message,
        )
        return log_user_command(message)
    clear_code = input_code.split()
    if len(clear_code) <= 1 or len(clear_code) > 2:
        return bot.send_message(
            message.chat.id,
            erorr_code_message,
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
            message.from_user.last_name,
        )
        return check_user_permissions(message)
    bot.send_message(
        message.chat.id,
        'Код не найден в системе!\n'
        'Запросите код у администратора проекта, '
        'либо используйте имеющийся.',
    )
    return log_user_command(message)


@bot.message_handler(commands=['updates', 'massmess'])
def mass_info_message(message):
    """
    Рассылка информации всем пользователям.
    - updates: для заготовленных обновлений
    - massmess: для любих сообщений (до 500 символов)
    """
    access = get_admin_access(message.chat.id)
    if access is None or access[1] != message.chat.id:
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
    input_message = message.text.split()
    if input_message[0] == '/updates':
        message_for_users = UPDATE_MESSAGE
    elif input_message[0] == '/massmess':
        message_for_users = ' '.join(input_message[1:])
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/massmess your_message\n'
            f'\nМаксимально {MAX_MESSAGE_SYMBOLS} символов!'
        )
        if (len(input_message) <= 1
           or len(' '.join(input_message[1:]))) > MAX_MESSAGE_SYMBOLS:
            bot.send_message(
                message.chat.id,
                erorr_code_message
            )
            return log_user_command(message)
    users = search_all_user_id()
    send_count = 0
    eror_count = 0
    for user in users:
        try:
            send_count += 1
            bot.send_message(chat_id=user[0], text=message_for_users)
        except Exception:
            eror_count += 1
            raise bot.send_message(
                message.chat.id,
                f'ошибка отправки пользователю с id № {user[0]}'
            )
        finally:
            continue
    bot.send_message(
        message.chat.id,
        text=(
            f'Сообщение успешно отправлено {send_count} пользователям!\n'
            f'\nСообщение не доставлено {eror_count} пользователям!'
        )
    )
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
        return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
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
        button_1 = types.KeyboardButton('О компании')
        button_2 = types.KeyboardButton('Адаптация')
        button_3 = types.KeyboardButton('Карьерное развитие')
        button_4 = types.KeyboardButton('Цикл управления талантами')
        button_5 = types.KeyboardButton('Стажировка')
        button_6 = types.KeyboardButton('ДМС и РВЛ')
        button_7 = types.KeyboardButton('Молодежная политика')
        button_8 = types.KeyboardButton('Обратная связь')
        button_9 = types.KeyboardButton('Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
            button_7,
            button_8,
            button_9,
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
        markup.add(button)
        parrent_path = 'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/'
        file_1 = open(f'{parrent_path}8.pdf', 'rb')
        filename_1 = ('Пропускной и внутреобъектовый режимы '
                      'ООО "Инженерно-технологический сервис"')
        file_2 = open(f'{parrent_path}ib.pdf', 'rb')
        filename_2 = 'Памятка по ИБ'
        file_3 = open(f'{parrent_path}ptvr.pdf', 'rb')
        filename_3 = ('Правила внутреннего трудового распорядка '
                      'ООО "Инженерно-технологический сервис"')
        file_4 = open(f'{parrent_path}vahta.pdf', 'rb')
        filename_4 = ('Положение о вахтовом методе работы '
                      'ООО "Инженерно-технологический сервис"')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
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
        document_1 = open(
            'prod_data/о_компании/новостная_лента/corp_portal/guide.pdf',
            'rb'
        )
        document_2 = open(
            'prod_data/о_компании/новостная_лента/corp_portal/enter.pdf',
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
            document_1,
            caption='Как через Интернет войти на Портал знаний',
            parse_mode="html",
        )
        bot.send_document(
            message.chat.id,
            document_2,
            caption='Как войти в личный кабинет на портале знаний',
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
        btn_8 = types.KeyboardButton('Буклеты для сотрудников')
        btn_9 = types.KeyboardButton('Книги для сотрудников')
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
        markup.add(button)

        parrent_path = 'prod_data/Адаптация/hoz_trans/'
        file_1 = open(f'{parrent_path}ES.pdf', 'rb')
        file_2 = open(f'{parrent_path}ITS.pdf', 'rb')
        file_3 = open(f'{parrent_path}NR.pdf', 'rb')

        filename_1 = ('Хозяйственное и транспортное обеспечение '
                      'ООО "Газпромнефть Энергосистемы"')
        filename_2 = ('Хозяйственное и транспортное обеспечение '
                      'ООО "Инженерно-технологический сервис"')
        filename_3 = ('Хозяйственное и транспортное обеспечение '
                      'ООО "Нефтесервисные решения"')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }

        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
            )

    # АДАПТАЦИЯ =
    elif message.text == 'Трудовой распорядок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        markup.add(button)

        parrent_path = 'prod_data/Адаптация/trudovoi_raspor/'
        document_1 = open(f'{parrent_path}es_trud.pdf', 'rb')
        document_2 = open(f'{parrent_path}its_trud.pdf', 'rb')
        document_3 = open(f'{parrent_path}nr_trud.pdf', 'rb')
        document_4 = open(f'{parrent_path}st_trud.pdf', 'rb')

        filename_1 = ('Трудовой распорядок в '
                      'ООО "Газпромнефть Энергосистемы"')
        filename_2 = ('Трудовой распорядок в '
                      'ООО "Инженерно-технологический Сервис"')
        filename_3 = ('Трудовой распорядок в ООО "Нефтесервисные Решения"')
        filename_4 = ('Трудовой распорядок в '
                      'ООО "Газпромнефть Сервисные технологии"')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }

        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
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
    elif message.text == 'Буклеты для сотрудников':
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
    elif message.text == 'Книги для сотрудников':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Адаптация')
        markup.add(btn)
        parrent_path = 'prod_data/Адаптация/книги_для_новых_сотрудников/'
        file_1 = open(f'{parrent_path}ES_book.pdf', 'rb')
        file_2 = open(f'{parrent_path}NR_book.pdf', 'rb')
        file_3 = open(f'{parrent_path}ITS_book.pdf', 'rb')
        file_4 = open(f'{parrent_path}ST_book.pdf', 'rb')
        filename_1 = ('Книга для нового сотрудника '
                      'ООО "Газпромнефть Энергосистемы".')
        filename_2 = ('Книга для нового сотрудника '
                      'ООО "Нефтесервисные решения".')
        filename_3 = ('Книга для нового сотрудника '
                      'ООО "Инженерно-технологический сервис".')
        filename_4 = ('Книга для нового сотрудника '
                      'ООО "Газпромнефть Сервисные технологии".')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, document in files_dict.items():
            bot.send_document(
                message.chat.id,
                document=document,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
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
        markup.add(btn)
        parrent_path = 'prod_data/ДМС/ГПН_ЭС/ДМС/'
        documents = {
            'Памятка по лечению': f'{parrent_path}памятка_ДМС_2023.pdf',
            'Перечень поликлиник': f'{parrent_path}med_list.pdf',
            'Программа ДМС': f'{parrent_path}dms.pdf',
        }
        media_list = []
        for doc_name, doc_path in documents.items():
            file = open(doc_path, 'rb')
            new_file = telebot.types.InputMediaDocument(
                file,
                caption=doc_name,
                parse_mode='html'
            )
            media_list.append(new_file)
        bot.send_media_group(message.chat.id, media=media_list)

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
        button = types.KeyboardButton(
            '🔙 вернуться в раздел Цикл управления талантами'
        )
        markup.add(button)

        parrent_path = 'prod_data/Цикл_управления_талантами/Регулярная_оценка/'
        file_1 = open(f'{parrent_path}Процедуры.pdf', 'rb')
        file_2 = open(f'{parrent_path}для_сотрудников.pdf', 'rb')
        filename_1 = 'Процедуры ежегодной оценки в ГПН'
        filename_2 = 'Регулярная оценка для сотрудников'

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
            )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Комиссия по оценке вклада':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('🔙 вернуться в раздел Регулярная оценка')
        markup.add(btn)

        parrent_path = 'prod_data/Цикл_управления_талантами/Регулярная_оценка/'
        file = open(f'{parrent_path}Комиссия.pdf', 'rb')
        bot.send_document(
            message.chat.id,
            file,
            caption='Комиссия по оценке вклада для сотрудников',
            parse_mode="html",
            reply_markup=markup,
        )

    # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
    elif message.text == 'Диалоги об эффективности':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("смотреть видео",
                   url="https://youtu.be/O2JyX9iL8Hs"))

        parrent_path = 'prod_data/Цикл_управления_талантами/Диалоги_об_эффективности/'
        file_1 = open(f'{parrent_path}Инструкция.pdf', 'rb')
        file_2 = open(f'{parrent_path}ДоЭФ.PNG', 'rb')
        filename_1 = 'Инструкция по чтению отчета регулярной оценки 2023'
        filename_2 = 'Помятка для сотрудника'

        bot.send_message(
            message.chat.id,
            'Диалог об эффективности',
            reply_markup=markup,
        )

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
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
        button_1 = types.KeyboardButton('НТК МС')
        button_2 = types.KeyboardButton('СЛЕТ МС')
        button_3 = types.KeyboardButton(
            '🔙 вернуться в раздел Молодежная политика'
        )
        markup.add(button_1, button_2, button_3)
        bot.send_message(
            message.from_user.id,
            "Молодежный совет",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'НТК МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в '
                                      'раздел Развитие молодых специалистов')
        markup.add(button)

        parrent_path = ('prod_data/Молодежная_политика'
                        '/Развитие_молодых_специалистов/НТК/')

        file_1 = open(f'{parrent_path}Заявка_Шаблон.docx', 'rb')
        file_2 = open(f'{parrent_path}Шаблон_одностраничника.pptx', 'rb')
        file_3 = open(f'{parrent_path}Шаблон_презентации.pptx', 'rb')
        file_4 = open(f'{parrent_path}dk.pdf', 'rb')
        filename_1 = 'Заявка - Шаблон'
        filename_2 = 'Шаблон одностраничника'
        filename_3 = 'Шаблон презентации'
        filename_4 = 'Дорожная карта'

        bot.send_message(message.from_user.id, ABOUT_NTK, reply_markup=markup)

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
                reply_markup=markup,
            )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'СЛЕТ МС':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 вернуться в '
                                      'раздел Развитие молодых специалистов')
        markup.add(button)

        file = open(
            'prod_data/Молодежная_политика/'
            'Развитие_молодых_специалистов/Слет_МС/Слет_МС.pptx',
            'rb',
        )

        bot.send_document(
            message.chat.id,
            file,
            caption='Слет МС',
            parse_mode="html",
            reply_markup=markup,
        )

    # БЛАНКИ ЗАЯВЛЕНИЙ
    elif (message.text == 'Бланки заявлений'
          or message.text == '🔙 вернуться в раздел Бланки заявлений'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button_1 = types.KeyboardButton('Авансовый отчет')
        button_2 = types.KeyboardButton('Банковские реквизиты')
        button_3 = types.KeyboardButton('Изменение трудового договора')
        button_4 = types.KeyboardButton('Оформление отпусков')
        button_5 = types.KeyboardButton('Прекращение трудового договора')
        button_6 = types.KeyboardButton('Рождение ребенка')
        button_7 = types.KeyboardButton('Учет рабочего времени')
        button_8 = types.KeyboardButton('🔙 Главное меню')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
            button_7,
            button_8,
        )
        bot.send_message(
            message.from_user.id,
            'Бланки заявлений',
            reply_markup=markup,
        )

    elif (
        message.text == 'Учет рабочего времени'
        or message.text == '🔙 вернуться в раздел '
        'Учет рабочего времени'
    ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('Изменение графика работы')
        button_2 = types.KeyboardButton('Исполнение гос.обязанностей')
        button_3 = types.KeyboardButton('Простой, задержка в пути')
        button_4 = types.KeyboardButton('Работа в выходной день')
        button_5 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
        )
        bot.send_message(
            message.chat.id,
            'Учет рабочего времени',
            reply_markup=markup,
        )

    elif message.text == 'Работа в выходной день':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Работа в выходной день {ES}')
        button_2 = types.KeyboardButton(f'Работа в выходной день {NR}')
        button_3 = types.KeyboardButton(f'Работа в выходной день {ST}')
        button_4 = types.KeyboardButton(f'Работа в выходной день {ITS}')
        button_5 = types.KeyboardButton(f'Работа в выходной день {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Учет рабочего времени')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Работа в выходной день',
            reply_markup=markup,
        )

    elif message.text == f'Работа в выходной день {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ES/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Работа в выходной день {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ITS/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Работа в выходной день {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/NNGGF/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Работа в выходной день {NR}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/NR/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = ('Служебная записка на привлечение к работе '
                      'в выходные дни')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Работа в выходной день {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ST/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == 'Простой, задержка в пути':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Простой, задержка в пути {ES}')
        # button_2 = types.KeyboardButton(f'Простой, задержка в пути {NR}')
        button_3 = types.KeyboardButton(f'Простой, задержка в пути {ST}')
        button_4 = types.KeyboardButton(f'Простой, задержка в пути {ITS}')
        button_5 = types.KeyboardButton(f'Простой, задержка в пути {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Учет рабочего времени')
        markup.add(
            button_1,
            # button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Простой, задержка в пути',
            reply_markup=markup,
        )

    elif message.text == f'Простой, задержка в пути {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/ES/'
        file_1 = open(f'{parrent_path}SZ.docx', 'rb')
        file_2 = open(f'{parrent_path}list.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Простой, задержка в пути {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/ITS/'
        file_1 = open(f'{parrent_path}SZ.docx', 'rb')
        file_2 = open(f'{parrent_path}list.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Простой, задержка в пути {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/NNGGF/'
        file_1 = open(f'{parrent_path}SZ.docx', 'rb')
        file_2 = open(f'{parrent_path}list.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Простой, задержка в пути {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/ST/'
        file_1 = open(f'{parrent_path}SZ.docx', 'rb')
        file_2 = open(f'{parrent_path}list.docx', 'rb')
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Исполнение гос.обязанностей':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Исполнение гос.обязанностей {ES}')
        # button_2 = types.KeyboardButton(f'Исполнение гос.обязанностей {NR}')
        button_3 = types.KeyboardButton(f'Исполнение гос.обязанностей {ST}')
        button_4 = types.KeyboardButton(f'Исполнение гос.обязанностей {ITS}')
        button_5 = types.KeyboardButton(f'Исполнение гос.обязанностей {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Учет рабочего времени')
        markup.add(
            button_1,
            # button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Исполнение гос.обязанностей',
            reply_markup=markup,
        )

    elif message.text == f'Исполнение гос.обязанностей {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/government_duties/ES/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = ('Ш-14.03.05-03 Заявление об исполнении '
                      'государственных или общественных обязанностей')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )

    elif message.text == f'Исполнение гос.обязанностей {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/government_duties/ITS/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = ('Ш-14.03.05-03 Заявление об исполнении '
                      'государственных или общественных обязанностей')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )

    elif message.text == f'Исполнение гос.обязанностей {NNGGF}':
        parrent_path = ('prod_data/blanks/time_tracking/government_duties/'
                        'NNGGF/')
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = ('Ш-14.03.05-03 Заявление об исполнении '
                      'государственных или общественных обязанностей')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )

    elif message.text == f'Исполнение гос.обязанностей {ST}':
        parrent_path = ('prod_data/blanks/time_tracking/government_duties/ST/')
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        filename_1 = ('Ш-14.03.05-03 Заявление об исполнении '
                      'государственных или общественных обязанностей')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )

    elif message.text == 'Изменение графика работы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Изменение графика {ES}')
        button_2 = types.KeyboardButton(f'Изменение графика {NR}')
        button_3 = types.KeyboardButton(f'Изменение графика {ST}')
        button_4 = types.KeyboardButton(f'Изменение графика {ITS}')
        button_5 = types.KeyboardButton(f'Изменение графика {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Учет рабочего времени')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Рождение ребенка',
            reply_markup=markup,
        )

    elif message.text == f'Изменение графика {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ES/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        file_2 = open(f'{parrent_path}baby_cancel.docx', 'rb')
        file_3 = open(f'{parrent_path}change.docx', 'rb')
        file_4 = open(f'{parrent_path}new.docx', 'rb')
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Изменение графика {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ITS/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        file_2 = open(f'{parrent_path}baby_cancel.docx', 'rb')
        file_3 = open(f'{parrent_path}change.docx', 'rb')
        file_4 = open(f'{parrent_path}new.docx', 'rb')
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Изменение графика {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/NNGGF/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        file_2 = open(f'{parrent_path}change.docx', 'rb')
        file_3 = open(f'{parrent_path}new.docx', 'rb')
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_3 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Изменение графика {NR}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/NR/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        file_2 = open(f'{parrent_path}change_grafik.docx', 'rb')
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Изменение графика {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ST/'
        file_1 = open(f'{parrent_path}main.docx', 'rb')
        file_2 = open(f'{parrent_path}baby_cancel.docx', 'rb')
        file_3 = open(f'{parrent_path}change.docx', 'rb')
        file_4 = open(f'{parrent_path}new.docx', 'rb')
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Рождение ребенка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Рождение ребенка {ES}')
        button_2 = types.KeyboardButton(f'Рождение ребенка {NR}')
        button_3 = types.KeyboardButton(f'Рождение ребенка {ST}')
        button_4 = types.KeyboardButton(f'Рождение ребенка {ITS}')
        button_5 = types.KeyboardButton(f'Рождение ребенка {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Рождение ребенка',
            reply_markup=markup,
        )

    elif message.text == f'Рождение ребенка {ES}':
        parrent_path = 'prod_data/blanks/baby_born/ES/'
        file_1 = open(f'{parrent_path}rodi.doc', 'rb')
        file_2 = open(f'{parrent_path}ranie_rodi.doc', 'rb')
        file_3 = open(f'{parrent_path}posobie_3.doc', 'rb')
        file_4 = open(f'{parrent_path}premia.doc', 'rb')
        file_5 = open(f'{parrent_path}posobie_1.5.doc', 'rb')
        filename_1 = ('Ш-14.03.06-13 Заявление об отпуске '
                      'по беременности и родам')
        filename_2 = ('Ш-14.03.06-14 Заявление о выплате пособия '
                      'за постановку на учет в ранние сроки беременности')
        filename_3 = ('Ш-14.03.06-15 Заявление об отпуске '
                      'по уходу за ребенком до 3х лет')
        filename_4 = ('Ш-14.03.06-16 Заявление о выплате '
                      'единовременного пособия по рождению ребенка')
        filename_5 = ('Ш-14.03.06-17 Заявление о выплате пособия '
                      'по уходу за ребенком до 1.5 лет')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Рождение ребенка {ITS}':
        parrent_path = 'prod_data/blanks/baby_born/ITS/'
        file_1 = open(f'{parrent_path}rodi.doc', 'rb')
        file_2 = open(f'{parrent_path}ranie_rodi.doc', 'rb')
        file_3 = open(f'{parrent_path}posobie_3.doc', 'rb')
        file_4 = open(f'{parrent_path}premia.doc', 'rb')
        file_5 = open(f'{parrent_path}posobie_1.5.doc', 'rb')
        filename_1 = ('Ш-14.03.06-13 Заявление об отпуске '
                      'по беременности и родам')
        filename_2 = ('Ш-14.03.06-14 Заявление о выплате пособия '
                      'за постановку на учет в ранние сроки беременности')
        filename_3 = ('Ш-14.03.06-15 Заявление об отпуске '
                      'по уходу за ребенком до 3х лет')
        filename_4 = ('Ш-14.03.06-16 Заявление о выплате '
                      'единовременного пособия по рождению ребенка')
        filename_5 = ('Ш-14.03.06-17 Заявление о выплате пособия '
                      'по уходу за ребенком до 1.5 лет')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Рождение ребенка {NNGGF}':
        parrent_path = 'prod_data/blanks/baby_born/NNGGF/'
        file_1 = open(f'{parrent_path}prervat_otpusk.docx', 'rb')
        file_2 = open(f'{parrent_path}otpusk_rodi.doc', 'rb')
        file_3 = open(f'{parrent_path}posobie_ranie.doc', 'rb')
        file_4 = open(f'{parrent_path}otpusk_uhod.doc', 'rb')
        file_5 = open(f'{parrent_path}premia.doc', 'rb')
        file_6 = open(f'{parrent_path}posobie.doc', 'rb')
        filename_1 = ('Ш-14.03.05-04 Заявление о досрочном '
                      'выходе из отпуска по уходу за ребенком_ГПН-ННГГФ')
        filename_2 = ('Ш-14.03.06-13 Заявление об отпуске '
                      'по беременности и родам_2 круг')
        filename_3 = ('Ш-14.03.06-14 Заявление о выплате пособия за '
                      'постановку на учет в ранние сроки беременности_2 круг')
        filename_4 = ('Ш-14.03.06-15 Заявление об отпуске по '
                      'уходу за ребенком до 3х лет')
        filename_5 = ('Ш-14.03.06-16 Заявление о выплате единовременного '
                      'пособия по рождению ребенка_2 круг')
        filename_6 = ('Ш-14.03.06-17 Заявление о выплате пособия по '
                      'уходу за ребенком до 1.5 лет_2 круг')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
            filename_6: file_6,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Рождение ребенка {NR}':
        parrent_path = 'prod_data/blanks/baby_born/NR/'
        file_1 = open(f'{parrent_path}premia.docx', 'rb')
        filename_1 = 'Заявление ГПН-НС_материальная помощь на рождение'
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Рождение ребенка {ST}':
        parrent_path = 'prod_data/blanks/baby_born/ST/'
        file_1 = open(f'{parrent_path}rodi.doc', 'rb')
        file_2 = open(f'{parrent_path}ranie_rodi.doc', 'rb')
        file_3 = open(f'{parrent_path}posobie_3.doc', 'rb')
        file_4 = open(f'{parrent_path}premia.doc', 'rb')
        file_5 = open(f'{parrent_path}posobie_1.5.doc', 'rb')
        filename_1 = ('Ш-14.03.06-13 Заявление об отпуске '
                      'по беременности и родам')
        filename_2 = ('Ш-14.03.06-14 Заявление о выплате пособия '
                      'за постановку на учет в ранние сроки беременности')
        filename_3 = ('Ш-14.03.06-15 Заявление об отпуске '
                      'по уходу за ребенком до 3х лет')
        filename_4 = ('Ш-14.03.06-16 Заявление о выплате '
                      'единовременного пособия по рождению ребенка')
        filename_5 = ('Ш-14.03.06-17 Заявление о выплате пособия '
                      'по уходу за ребенком до 1.5 лет')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Прекращение трудового договора':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Прекращение ТД {ES}')
        button_2 = types.KeyboardButton(f'Прекращение ТД {NR}')
        button_3 = types.KeyboardButton(f'Прекращение ТД {ST}')
        button_4 = types.KeyboardButton(f'Прекращение ТД {ITS}')
        button_5 = types.KeyboardButton(f'Прекращение ТД {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Прекращение ТД',
            reply_markup=markup,
        )

    elif message.text == f'Прекращение ТД {ES}':
        parrent_path = 'prod_data/blanks/termination_contract/ES/'
        file_1 = open(f'{parrent_path}questionnaire.doc', 'rb')
        file_2 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = 'Ш-14.03.03-01 Анкета при увольнении'
        filename_2 = 'Ш-14.03.03-02 Заявление об увольнении'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Прекращение ТД {ITS}':
        parrent_path = 'prod_data/blanks/termination_contract/ITS/'
        file_1 = open(f'{parrent_path}questionnaire.doc', 'rb')
        file_2 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = 'Ш-14.03.03-01 Анкета при увольнении'
        filename_2 = 'Ш-14.03.03-02 Заявление об увольнении'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Прекращение ТД {NNGGF}':
        parrent_path = 'prod_data/blanks/termination_contract/NNGGF/'
        file_1 = open(f'{parrent_path}questionnaire.doc', 'rb')
        file_2 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = 'Ш-14.03.03-01 Анкета при увольнении'
        filename_2 = 'Ш-14.03.03-02 Заявление об увольнении'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Прекращение ТД {NR}':
        parrent_path = 'prod_data/blanks/termination_contract/NR/'
        file_1 = open(f'{parrent_path}otpravka_trudovoi.doc', 'rb')
        file_2 = open(f'{parrent_path}perevod.doc', 'rb')
        file_3 = open(f'{parrent_path}cancel.docx', 'rb')
        file_4 = open(f'{parrent_path}uvolnenie.doc', 'rb')
        file_5 = open(f'{parrent_path}otpusk_uvolnenie.doc', 'rb')
        filename_1 = 'Заявление на отправку трудовой книжки'
        filename_2 = 'Заявление об увольнении в порядке перевода'
        filename_3 = 'Отзыв увольнения'
        filename_4 = 'Ш-14.03.03-02 Заявление об увольнении'
        filename_5 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении отпуска с увольнением')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Прекращение ТД {ST}':
        parrent_path = 'prod_data/blanks/termination_contract/ST/'
        file_1 = open(f'{parrent_path}raspiska.docx', 'rb')
        file_2 = open(f'{parrent_path}questionnaire.doc', 'rb')
        file_3 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = 'Расписка при увольнении'
        filename_2 = 'Ш-14.03.03-01 Анкета при увольнении'
        filename_3 = 'Ш-14.03.03-02 Заявление об увольнении'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif (
        message.text == 'Оформление отпусков'
        or message.text == '🔙 вернуться в раздел '
        'Оформление отпусков'
    ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('Другие виды отпусков')
        button_2 = types.KeyboardButton('Отмена, отзыв из отпуска')
        button_3 = types.KeyboardButton('Отпуск без сохранения зп')
        button_4 = types.KeyboardButton('Перенос, продление отпуска')
        button_5 = types.KeyboardButton('Сдача крови')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Оформление отпусков',
            reply_markup=markup,
        )

    elif message.text == 'Сдача крови':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Сдача крови {ES}')
        button_2 = types.KeyboardButton(f'Сдача крови {NR}')
        button_3 = types.KeyboardButton(f'Сдача крови {ST}')
        button_4 = types.KeyboardButton(f'Сдача крови {ITS}')
        button_5 = types.KeyboardButton(f'Сдача крови {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Оформление отпусков')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Сдача крови',
            reply_markup=markup,
        )

    elif message.text == f'Сдача крови {ES}':
        parrent_path = ('prod_data/blanks/vacation_registration/blood/ES/')
        file_1 = open(f'{parrent_path}osvobodit.doc', 'rb')
        file_2 = open(f'{parrent_path}drugoi.doc', 'rb')
        file_3 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-23 Заявление об освобождении '
                      'от работы в день сдачи крови')
        filename_2 = ('Ш-14.03.06-24 Заявление о предоставлении '
                      'другого дня отдыха в связи со сдачей крови')
        filename_3 = ('Ш-14.03.06-26 Заявление о предоставлении '
                      'дополнительного дня отдыха в связи со сдачей крови')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Сдача крови {ITS}':
        parrent_path = ('prod_data/blanks/vacation_registration/blood/ITS/')
        file_1 = open(f'{parrent_path}osvobodit.doc', 'rb')
        file_2 = open(f'{parrent_path}drugoi.doc', 'rb')
        file_3 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-23 Заявление об освобождении '
                      'от работы в день сдачи крови')
        filename_2 = ('Ш-14.03.06-24 Заявление о предоставлении '
                      'другого дня отдыха в связи со сдачей крови')
        filename_3 = ('Ш-14.03.06-26 Заявление о предоставлении '
                      'дополнительного дня отдыха в связи со сдачей крови')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Сдача крови {NNGGF}':
        parrent_path = ('prod_data/blanks/vacation_registration/blood/NNGGF/')
        file_1 = open(f'{parrent_path}osvobodit.doc', 'rb')
        file_2 = open(f'{parrent_path}drugoi.doc', 'rb')
        file_3 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-23 Заявление об освобождении '
                      'от работы в день сдачи крови')
        filename_2 = ('Ш-14.03.06-24 Заявление о предоставлении '
                      'другого дня отдыха в связи со сдачей крови')
        filename_3 = ('Ш-14.03.06-26 Заявление о предоставлении '
                      'дополнительного дня отдыха в связи со сдачей крови')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Сдача крови {NR}':
        parrent_path = ('prod_data/blanks/vacation_registration/blood/NR/')
        file_1 = open(f'{parrent_path}drugoi.doc', 'rb')
        file_2 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-24 Заявление о предоставлении '
                      'другого дня отдыха в связи со сдачей крови')
        filename_2 = ('Ш-14.03.06-26 Заявление о предоставлении '
                      'дополнительного дня отдыха в связи со сдачей крови')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Сдача крови {ST}':
        parrent_path = ('prod_data/blanks/vacation_registration/blood/ST/')
        file_1 = open(f'{parrent_path}osvobodit.doc', 'rb')
        file_2 = open(f'{parrent_path}drugoi.doc', 'rb')
        file_3 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-23 Заявление об освобождении '
                      'от работы в день сдачи крови')
        filename_2 = ('Ш-14.03.06-24 Заявление о предоставлении '
                      'другого дня отдыха в связи со сдачей крови')
        filename_3 = ('Ш-14.03.06-26 Заявление о предоставлении '
                      'дополнительного дня отдыха в связи со сдачей крови')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Перенос, продление отпуска':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Перенос, продление отпуска {ES}')
        button_2 = types.KeyboardButton(f'Перенос, продление отпуска {NR}')
        button_3 = types.KeyboardButton(f'Перенос, продление отпуска {ST}')
        button_4 = types.KeyboardButton(f'Перенос, продление отпуска {ITS}')
        button_5 = types.KeyboardButton(f'Перенос, продление отпуска {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Оформление отпусков')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Перенос, продление отпуска',
            reply_markup=markup,
        )

    elif message.text == f'Перенос, продление отпуска {ES}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'transfer_vacation/ES/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.doc', 'rb')
        file_3 = open(f'{parrent_path}health.doc', 'rb')
        filename_1 = 'Ш-14.03.06-05 Заявление о переносе отпуска'
        filename_2 = 'Ш-14.03.06-06 Служебная записка о переносе отпуска'
        filename_3 = ('Ш-14.03.06-30 Заявление о продлении-переносе '
                      'отпуска в связи с временной нетрудоспособностью')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Перенос, продление отпуска {ITS}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'transfer_vacation/ITS/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.doc', 'rb')
        file_3 = open(f'{parrent_path}health.doc', 'rb')
        filename_1 = 'Ш-14.03.06-05 Заявление о переносе отпуска'
        filename_2 = 'Ш-14.03.06-06 Служебная записка о переносе отпуска'
        filename_3 = ('Ш-14.03.06-30 Заявление о продлении-переносе '
                      'отпуска в связи с временной нетрудоспособностью')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Перенос, продление отпуска {NNGGF}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'transfer_vacation/NNGGF/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.doc', 'rb')
        file_3 = open(f'{parrent_path}health.doc', 'rb')
        filename_1 = 'Ш-14.03.06-05 Заявление о переносе отпуска'
        filename_2 = 'Ш-14.03.06-06 Служебная записка о переносе отпуска'
        filename_3 = ('Ш-14.03.06-30 Заявление о продлении-переносе '
                      'отпуска в связи с временной нетрудоспособностью')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Перенос, продление отпуска {NR}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'transfer_vacation/NR/')
        file_1 = open(f'{parrent_path}application.docx', 'rb')
        file_2 = open(f'{parrent_path}health.docx', 'rb')
        filename_1 = 'Перенос дней отдыха за РВД'
        filename_2 = 'Перенос отпуска'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Перенос, продление отпуска {ST}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'transfer_vacation/ST/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.doc', 'rb')
        file_3 = open(f'{parrent_path}dop.doc', 'rb')
        file_4 = open(f'{parrent_path}health.doc', 'rb')
        filename_1 = 'Ш-14.03.06-05 Заявление о переносе отпуска'
        filename_2 = 'Ш-14.03.06-06 Служебная записка о переносе отпуска'
        filename_3 = ('Ш-14.03.06-07 Заявление о предоставлении '
                      'иного вида отпуска')
        filename_4 = ('Ш-14.03.06-30 Заявление о продлении-переносе '
                      'отпуска в связи с временной нетрудоспособностью')
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Отпуск без сохранения зп':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Отпуск без сохранения зп {ES}')
        button_2 = types.KeyboardButton(f'Отпуск без сохранения зп {NR}')
        button_3 = types.KeyboardButton(f'Отпуск без сохранения зп {ST}')
        button_4 = types.KeyboardButton(f'Отпуск без сохранения зп {ITS}')
        button_5 = types.KeyboardButton(f'Отпуск без сохранения зп {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Оформление отпусков')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Отпуск без сохранения зп',
            reply_markup=markup,
        )

    elif message.text == f'Отпуск без сохранения зп {ES}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'vacation_without_money/ES/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-21 Заявление о предоставлении '
                      'отпуска без сохранения заработной платы')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Отпуск без сохранения зп {ITS}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'vacation_without_money/ITS/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-21 Заявление о предоставлении '
                      'отпуска без сохранения заработной платы')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Отпуск без сохранения зп {NNGGF}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'vacation_without_money/NNGGF/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-21 Заявление о предоставлении '
                      'отпуска без сохранения заработной платы')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Отпуск без сохранения зп {NR}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'vacation_without_money/NR/')
        file_1 = open(f'{parrent_path}application.docx', 'rb')
        filename_1 = 'Заявление о предоставлении отпуска'
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Отпуск без сохранения зп {ST}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'vacation_without_money/ST/')
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-21 Заявление о предоставлении '
                      'отпуска без сохранения заработной платы')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == 'Отмена, отзыв из отпуска':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Отмена, отзыв из отпуска {ES}')
        button_2 = types.KeyboardButton(f'Отмена, отзыв из отпуска {NR}')
        button_3 = types.KeyboardButton(f'Отмена, отзыв из отпуска {ST}')
        button_4 = types.KeyboardButton(f'Отмена, отзыв из отпуска {ITS}')
        button_5 = types.KeyboardButton(f'Отмена, отзыв из отпуска {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Оформление отпусков')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Отмена, отзыв из отпуска',
            reply_markup=markup,
        )

    elif message.text == f'Отмена, отзыв из отпуска {ES}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'cancellation/ES/')
        file_1 = open(f'{parrent_path}SZ_otziv.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ_otmena.doc', 'rb')
        file_3 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-08 Служебная записка '
                      'об отзыве из отпуска')
        filename_2 = ('Ш-14.03.06-10 Служебная записка '
                      'об отмене отпуска')
        filename_3 = 'Ш-14.03.06-11 Заявление об отмене отпуска'

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Отмена, отзыв из отпуска {ITS}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'cancellation/ITS/')
        file_1 = open(f'{parrent_path}SZ_otziv.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ_otmena.doc', 'rb')
        file_3 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-08 Служебная записка '
                      'об отзыве из отпуска')
        filename_2 = ('Ш-14.03.06-10 Служебная записка '
                      'об отмене отпуска')
        filename_3 = 'Ш-14.03.06-11 Заявление об отмене отпуска'

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Отмена, отзыв из отпуска {NNGGF}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'cancellation/NNGGF/')
        file_1 = open(f'{parrent_path}SZ_otziv.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ_otmena.doc', 'rb')
        file_3 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-08 Служебная записка '
                      'об отзыве из отпуска')
        filename_2 = ('Ш-14.03.06-10 Служебная записка '
                      'об отмене отпуска')
        filename_3 = 'Ш-14.03.06-11 Заявление об отмене отпуска'

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Отмена, отзыв из отпуска {NR}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'cancellation/NR/')
        file_1 = open(f'{parrent_path}SZ_otziv.docx', 'rb')
        file_2 = open(f'{parrent_path}SZ_otmena.doc', 'rb')
        filename_1 = ('Ш-14.03.06-08 Служебная записка '
                      'об отзыве из отпуска')
        filename_2 = ('Ш-14.03.06-10 Служебная записка '
                      'об отмене отпуска')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Отмена, отзыв из отпуска {ST}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'cancellation/ST/')
        file_1 = open(f'{parrent_path}SZ_otziv.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ_otmena.doc', 'rb')
        file_3 = open(f'{parrent_path}application.doc', 'rb')
        filename_1 = ('Ш-14.03.06-08 Служебная записка '
                      'об отзыве из отпуска')
        filename_2 = ('Ш-14.03.06-10 Служебная записка '
                      'об отмене отпуска')
        filename_3 = 'Ш-14.03.06-11 Заявление об отмене отпуска'

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Другие виды отпусков':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Другие виды отпусков {ES}')
        button_2 = types.KeyboardButton(f'Другие виды отпусков {NR}')
        button_3 = types.KeyboardButton(f'Другие виды отпусков {ST}')
        button_4 = types.KeyboardButton(f'Другие виды отпусков {ITS}')
        button_5 = types.KeyboardButton(f'Другие виды отпусков {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Оформление отпусков')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Другие виды отпусков',
            reply_markup=markup,
        )

    elif message.text == f'Другие виды отпусков {ES}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'other_vacation/ES/')
        file_1 = open(f'{parrent_path}dop.doc', 'rb')
        file_2 = open(f'{parrent_path}main.doc', 'rb')
        filename_1 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении иного вида отпуска')
        filename_2 = ('Ш-14.03.06-29 Заявление о '
                      'предоставлении внепланового отпуска')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Другие виды отпусков {ITS}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'other_vacation/ITS/')
        file_1 = open(f'{parrent_path}dop.doc', 'rb')
        file_2 = open(f'{parrent_path}main.doc', 'rb')
        filename_1 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении иного вида отпуска')
        filename_2 = ('Ш-14.03.06-29 Заявление о '
                      'предоставлении внепланового отпуска')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Другие виды отпусков {NNGGF}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'other_vacation/NNGGF/')
        file_1 = open(f'{parrent_path}dop.doc', 'rb')
        file_2 = open(f'{parrent_path}main.doc', 'rb')
        filename_1 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении иного вида отпуска')
        filename_2 = ('Ш-14.03.06-29 Заявление о '
                      'предоставлении внепланового отпуска')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Другие виды отпусков {NR}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'other_vacation/NR/')
        file_1 = open(f'{parrent_path}weekend.docx', 'rb')
        file_2 = open(f'{parrent_path}family.doc', 'rb')
        file_3 = open(f'{parrent_path}moving.docx', 'rb')
        file_4 = open(f'{parrent_path}dop.docx', 'rb')
        file_5 = open(f'{parrent_path}arrangement.doc', 'rb')
        file_6 = open(f'{parrent_path}dop_2.doc', 'rb')
        filename_1 = ('Заявление на предоставление дня отдыха'
                      ' за РВД в командировке.')
        filename_2 = 'Заявление о предоставлении отпуска'
        filename_3 = 'Ш-05.08-07 Заявление на присоединение выходных дней'
        filename_4 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении иного вида отпуска')
        filename_5 = ('Ш-14.03.06-07 Заявление о предоставлении '
                      'иного вида отпуска ОБУСТРОЙСТВО')
        filename_6 = ('Ш-14.03.06-07 Заявление о '
                      'предоставлении доп. дней отпуска')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
            filename_4: file_4,
            filename_5: file_5,
            filename_6: file_6,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Другие виды отпусков {ST}':
        parrent_path = ('prod_data/blanks/vacation_registration/'
                        'other_vacation/ST/')
        file_1 = open(f'{parrent_path}dop.doc', 'rb')
        filename_1 = ('Ш-14.03.06-29 Заявление о '
                      'предоставлении внепланового отпуска')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif (
        message.text == 'Изменение трудового договора'
        or message.text == '🔙 вернуться в раздел '
        'Изменение трудового договора'
    ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('Дополнительная работа')
        button_2 = types.KeyboardButton('Переводы')
        button_3 = types.KeyboardButton('Режим рабочего времени')
        button_4 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
        )
        bot.send_message(
            message.chat.id,
            'Изменение трудового договора',
            reply_markup=markup,
        )

    elif message.text == 'Режим рабочего времени':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Режим рабочего времени {ES}')
        button_2 = types.KeyboardButton(f'Режим рабочего времени {NR}')
        button_3 = types.KeyboardButton(f'Режим рабочего времени {ST}')
        button_4 = types.KeyboardButton(f'Режим рабочего времени {ITS}')
        button_5 = types.KeyboardButton(f'Режим рабочего времени {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Изменение трудового договора')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Режим рабочего времени',
            reply_markup=markup,
        )

    elif message.text == f'Режим рабочего времени {ES}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/working_hours/ES/'
        file_1 = open(f'{parrent_path}work_down.doc', 'rb')
        file_2 = open(f'{parrent_path}change_work_hours.docx', 'rb')
        filename_1 = ('Ш-14.03.02-02 Заявление о снижении '
                      'норм выработки_норм обслуживания')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Режим рабочего времени {ITS}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/working_hours/ITS/'
        file_1 = open(f'{parrent_path}ITS_work_down.doc', 'rb')
        file_2 = open(f'{parrent_path}ITS_change_work_hours.docx', 'rb')
        filename_1 = ('Ш-14.03.02-02 Заявление о снижении '
                      'норм выработки_норм обслуживания_ООО ИТС')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени_ООО ИТС')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Режим рабочего времени {NNGGF}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/working_hours/ITS/'
        file_1 = open(f'{parrent_path}NNGGF_work_down.doc', 'rb')
        file_2 = open(f'{parrent_path}NNGGF_change_work_hours.docx', 'rb')
        filename_1 = ('Ш-14.03.02-02 Заявление о снижении '
                      'норм выработки_норм обслуживания_ГПН-ННГГФ')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени_ГПН-ННГГФ')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Режим рабочего времени {NR}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/working_hours/NR/'
        file_1 = open(f'{parrent_path}change_work_hours.docx', 'rb')
        filename_1 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Режим рабочего времени {ST}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/working_hours/ST/'
        file_1 = open(f'{parrent_path}work_down.doc', 'rb')
        file_2 = open(f'{parrent_path}change_work_hours.docx', 'rb')
        filename_1 = ('Ш-14.03.02-02 Заявление о снижении '
                      'норм выработки_норм обслуживания')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Переводы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Переводы {ES}')
        button_2 = types.KeyboardButton(f'Переводы {NR}')
        button_3 = types.KeyboardButton(f'Переводы {ST}')
        button_4 = types.KeyboardButton(f'Переводы {ITS}')
        button_5 = types.KeyboardButton(f'Переводы {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Изменение трудового договора')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Переводы',
            reply_markup=markup,
        )

    elif message.text == f'Переводы {ES}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/transfers/ES/'
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.docx', 'rb')
        file_3 = open(f'{parrent_path}application_health_risk_work.doc', 'rb')
        filename_1 = ('Ш-14.03.02-01 Заявление о переводе на другую работу')
        filename_2 = ('Ш-14.03.02-07 Служебная записка о переводе '
                      'на другую работу')
        filename_3 = ('Ш-14.03.02-15 Заявление о переводе '
                      'на другую работу в связи с беременностью')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Переводы {ITS}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/transfers/ITS/'
        file_1 = open(f'{parrent_path}ITS_application.doc', 'rb')
        file_2 = open(f'{parrent_path}ITS_SZ.docx', 'rb')
        file_3 = open(f'{parrent_path}ITS_application_health_risk_work.doc',
                      'rb')
        filename_1 = ('Ш-14.03.02-01 Заявление о переводе '
                      'на другую работу_ООО ИТС')
        filename_2 = ('Ш-14.03.02-07 Служебная записка о переводе '
                      'на другую работу_фин_ООО ИТС')
        filename_3 = ('Ш-14.03.02-15 Заявление о переводе '
                      'на другую работу в связи с беременностью_ООО ИТС')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Переводы {NNGGF}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/transfers/ITS/'
        file_1 = open(f'{parrent_path}NNGGF_application.doc', 'rb')
        file_2 = open(f'{parrent_path}NNGGF_SZ.docx', 'rb')
        file_3 = open(f'{parrent_path}NNGGF_application_health_risk_work.doc',
                      'rb')
        filename_1 = ('Ш-14.03.02-01 Заявление о переводе '
                      'на другую работу_ГПН-ННГГФ')
        filename_2 = ('Ш-14.03.02-07 Служебная записка о переводе '
                      'на другую работу_фин_ГПН_ННГГФ')
        filename_3 = ('Ш-14.03.02-15 Заявление о переводе '
                      'на другую работу в связи с беременностью_ГПН_ННГГФ')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Переводы {NR}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/transfers/NR/'
        file_1 = open(f'{parrent_path}application.docx', 'rb')
        filename_1 = ('Заявление на перевод')
        bot.send_document(
            message.chat.id,
            document=file_1,
            caption=filename_1,
            parse_mode="html",
        )

    elif message.text == f'Переводы {ST}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/transfers/ST/'
        file_1 = open(f'{parrent_path}application.doc', 'rb')
        file_2 = open(f'{parrent_path}SZ.docx', 'rb')
        filename_1 = ('Ш-14.03.02-01 Заявление о переводе '
                      'на другую работу')
        filename_2 = ('Ш-14.03.02-07 Служебная записка '
                      'о переводе на другую работу')

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                document=file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == 'Дополнительная работа':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Доп. работа {ES}')
        button_2 = types.KeyboardButton(f'Доп. работа {NR}')
        button_3 = types.KeyboardButton(f'Доп. работа {ST}')
        button_4 = types.KeyboardButton(f'Доп. работа {ITS}')
        button_5 = types.KeyboardButton(f'Доп. работа {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Изменение трудового договора')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Дополнительная работа',
            reply_markup=markup,
        )

    elif message.text == f'Доп. работа {ES}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/dop_work/ES/'
        file_1 = open(f'{parrent_path}SZ.doc', 'rb')
        filename_1 = ('Ш-14.03.02-10 Служебная записка '
                      'о поручении дополнительной работы')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Доп. работа {ITS}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/dop_work/ITS/'
        file_1 = open(f'{parrent_path}SZ_ITS.doc', 'rb')
        filename_1 = ('Ш-14.03.02-10 Служебная записка '
                      'о поручении дополнительной работы_ООО ИТС')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Доп. работа {NNGGF}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/dop_work/ITS/'
        file_1 = open(f'{parrent_path}SZ_NNGGF.doc', 'rb')
        filename_1 = ('Ш-14.03.02-10 Служебная записка '
                      'о поручении дополнительной работы_ГПН_ННГГФ')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Доп. работа {NR}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/dop_work/NR/'
        file_1 = open(f'{parrent_path}SZ.doc', 'rb')
        filename_1 = ('Ш-14.03.02-10 Служебная записка '
                      'о поручении дополнительной работы')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Доп. работа {ST}':
        parrent_path = 'prod_data/blanks/TK_RF_changes/dop_work/ST/'
        file_1 = open(f'{parrent_path}SZ.doc', 'rb')
        filename_1 = ('Ш-14.03.02-10 Служебная записка '
                      'о поручении дополнительной работы')
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == 'Банковские реквизиты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Банковские реквизиты {ES}')
        button_2 = types.KeyboardButton(f'Банковские реквизиты {NR}')
        button_3 = types.KeyboardButton(f'Банковские реквизиты {ST}')
        button_4 = types.KeyboardButton(f'Банковские реквизиты {ITS}')
        button_5 = types.KeyboardButton(f'Банковские реквизиты {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Банковские реквизиты',
            reply_markup=markup,
        )

    elif message.text == f'Банковские реквизиты {ES}':
        parrent_path = 'prod_data/blanks/bank_details/ES/'
        file_1 = open(f'{parrent_path}statement.doc', 'rb')
        filename_1 = 'Заявление на перечисление ЗП по реквизитам'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Банковские реквизиты {ITS}':
        parrent_path = 'prod_data/blanks/bank_details/ITS/'
        file_1 = open(f'{parrent_path}stateman_ITS.doc', 'rb')
        filename_1 = 'Заявление о принятии и смене банка и реквизитов'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Банковские реквизиты {NNGGF}':
        parrent_path = 'prod_data/blanks/bank_details/ITS/'
        file_1 = open(f'{parrent_path}stateman_NNGGF.doc', 'rb')
        filename_1 = 'Заявление о принятии и смене банка и реквизитов'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Банковские реквизиты {NR}':
        parrent_path = 'prod_data/blanks/bank_details/NR/'
        file_1 = open(f'{parrent_path}statement.docx', 'rb')
        filename_1 = 'Заявление на перечисление ЗП по реквизитам'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Банковские реквизиты {ST}':
        parrent_path = 'prod_data/blanks/bank_details/ST/'
        file_1 = open(f'{parrent_path}statement.doc', 'rb')
        filename_1 = 'Заявление на перечисление ЗП по реквизитам'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == 'Авансовый отчет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Авансовый бланки {ES}')
        button_2 = types.KeyboardButton(f'Авансовый бланки {NR}')
        button_3 = types.KeyboardButton(f'Авансовый бланки {ST}')
        button_4 = types.KeyboardButton(f'Авансовый бланки {ITS}')
        button_5 = types.KeyboardButton(f'Авансовый бланки {NNGGF}')
        button_6 = types.KeyboardButton('🔙 вернуться в '
                                        'раздел Бланки заявлений')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.chat.id,
            'Авансовый отчет',
            reply_markup=markup,
        )

    elif message.text == f'Авансовый бланки {ES}':
        parrent_path = 'prod_data/blanks/avansov/ES/'
        file_1 = open(f'{parrent_path}blank.doc', 'rb')
        file_2 = open(f'{parrent_path}info.docx', 'rb')
        filename_1 = 'Авансовый отчет - бланк'
        filename_2 = 'Инструкция по заполнению АО'

        bot.send_message(
            message.from_user.id,
            f'Авансовый бланки {ES}',
        )

        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
        }
        for caption, file in files_dict.items():
            bot.send_document(
                message.chat.id,
                file,
                caption=caption,
                parse_mode="html",
            )

    elif message.text == f'Авансовый бланки {NR}':
        parrent_path = 'prod_data/blanks/avansov/NR/'
        file_1 = open(f'{parrent_path}SOP.pdf', 'rb')
        filename_1 = 'СОП по оформлению отчета по командировке с 01.10.23'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Авансовый бланки {ITS}':
        parrent_path = 'prod_data/blanks/avansov/ITS/'
        file_1 = open(f'{parrent_path}blank_1.xls', 'rb')
        filename_1 = 'Бланк авансового отчета'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Авансовый бланки {NNGGF}':
        parrent_path = 'prod_data/blanks/avansov/ITS/'
        file_1 = open(f'{parrent_path}blank_2.xls', 'rb')
        filename_1 = 'Бланк авансового отчета'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Авансовый бланки {ST}':
        parrent_path = 'prod_data/blanks/avansov/ST/'
        file_1 = open(f'{parrent_path}blank.doc', 'rb')
        filename_1 = 'Бланк авансового отчета'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == 'Обратная связь':
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
    return log_user_command(message)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    """Ловим отправленные пользователем изобращения."""
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        log_photo(message)
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')

    bot.send_message(
        message.chat.id,
        text=(
            '''
            У меня нет глаз,
            я не понимаю что на этой картинке.\n'
            Давайте продолжим работать в меню.
            '''
        ),
    )
    return log_photo(message)


@bot.message_handler(content_types=['sticker'])
def get_user_stiсker(message):
    """Ловим отправленные пользователем стикеры."""
    check_user = get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        log_sticker(message)
        return bot.send_message(message.chat.id,
                                'Вы не зарегистрированны в системе!')

    bot.send_message(
        message.chat.id,
        text=(
            '''
            У меня нет глаз, я не вижу этот стикер.
            Давайте продолжим работать в меню.
            '''
        ),
    )
    return log_sticker(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
