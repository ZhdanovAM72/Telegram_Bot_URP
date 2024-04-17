import telebot
from telebot import types

from bot.bot_command import BaseBotCommands
from bot.content_processor import BaseContentProcessor
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command
# from updates import UPDATE_MESSAGE
from bot.constant import (
    ES, ITS, NR, NNGGF, ST,
    ABOUT_NTK,
    NOT_REGISTERED,
)
from bot.content_processor.text.base import BaseTextMenu
from bot import bot, STOP_COMMAND


@bot.message_handler(commands=['admin'])
def admin(message: telebot.types.Message):
    """"Проверяем права администратора."""
    BaseBotCommands.admin_commands(message)


@bot.message_handler(commands=['updatecode'])
def update_code(message: telebot.types.Message):
    """Обновляем код в БД."""
    BaseBotCommands.update_code(message)


@bot.message_handler(commands=['createmoderator'])
def create_moderator(message: telebot.types.Message):
    """Создаем модератора."""
    BaseBotCommands.create_moderator(message)


@bot.message_handler(commands=['moderator'])
def moderator(message: telebot.types.Message):
    """"Проверяем права модератора."""
    BaseBotCommands.moderator_commands(message)


@bot.message_handler(commands=['deleteuser', 'deletecode'])
def delete_user(message: telebot.types.Message):
    """Удаление пользователей."""
    BaseBotCommands.delete_user_from_db(message)


@bot.message_handler(commands=['dbinfo'])
def export_db(message: telebot.types.Message):
    """Экспортируем БД."""
    BaseBotCommands.export_info(message)


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
    BaseBotCommands.create_code(message)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    """Начало работы в ботом."""
    BaseBotCommands.start(message)


@bot.message_handler(commands=['code'])
def register_user(message):
    """Определяем права пользователя."""
    BaseBotCommands.register(message)


# @bot.message_handler(commands=['updates', 'massmess'])
# def mass_info_message(message):
#     """
#     Рассылка информации всем пользователям.
#     - updates: для заготовленных обновлений
#     - massmess: для любых сообщений (до 500 символов)
#     """
#     access = get_admin_access(message.chat.id)
#     if access is None or access[1] != message.chat.id:
#         return bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
#     input_message = message.text.split()
#     if input_message[0] == '/updates':
#         message_for_users = UPDATE_MESSAGE
#     elif input_message[0] == '/massmess':
#         message_for_users = ' '.join(input_message[1:])
#         erorr_code_message = (
#             'Команда использована неверно, '
#             'введите запрос как показано на примере\!\n'  # noqa W605
#             'Пример: \n\/massmess your_message\n'  # noqa W605
#             f'\nМаксимально *{MAX_MESSAGE_SYMBOLS}* символов\!'  # noqa W605
#         )
#         if (len(input_message) <= 1
#            or len(' '.join(input_message[1:]))) > MAX_MESSAGE_SYMBOLS:
#             bot.send_message(
#                 message.chat.id,
#                 erorr_code_message,
#                 parse_mode='MarkdownV2',
#             )
#             return log_user_command(message)
#     users = search_all_user_id()
#     send_count = 0
#     eror_count = 0
#     for user in users:
#         try:
#             bot.send_message(
#                 chat_id=user[0],
#                 text=message_for_users,
#             )
#             send_count += 1
#         except Exception:
#             eror_count += 1
#             raise bot.send_message(
#                 message.chat.id,
#                 f'ошибка отправки пользователю с id № *{user[0]}*',
#                 parse_mode='MarkdownV2',
#             )
#         finally:
#             continue
#     bot.send_message(
#         message.chat.id,
#         text=(
#             f'Сообщение успешно отправлено *{send_count}* пользователям\!\n'  # noqa W605
#             f'\nСообщение не доставлено *{eror_count}* пользователям\!'  # noqa W605
#         ),
#         parse_mode='MarkdownV2'
#     )
#     return log_user_command(message)


@bot.message_handler(commands=[STOP_COMMAND])
def stop(message: telebot.types.Message):
    """Останавливаем работу бота."""
    BaseBotCommands.stop_command(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
    """
    Главное меню чат-бота с глубокой вложенностью
    и возможностью возврата к предыдущему пункту меню.
    """
    check_user = BaseBotSQLMethods.get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        return bot.send_message(message.chat.id, NOT_REGISTERED)

    menu_dict = {
        'Главное меню': BaseTextMenu.main_menu,
        '🔙 Главное меню': BaseTextMenu.main_menu,

        'О компании': BaseTextMenu.about_company,
        '🔙 вернуться в раздел О компании': BaseTextMenu.about_company,
        'Корпоративные ценности': BaseTextMenu.corporate_values,
        'Выбрать ДО': BaseTextMenu.choose_do,
        '🔙 вернуться в раздел Выбрать ДО': BaseTextMenu.choose_do,

        'Газпромнефть Сервисные технологии': BaseTextMenu.do_st,
        '🔙 вернуться в раздел Газпромнефть Сервисные технологии': BaseTextMenu.do_st,
        'Структура СТ': BaseTextMenu.structure_st,
        'История СТ': BaseTextMenu.history_st,

        'Нефтесервисные решения': BaseTextMenu.do_nr,
        '🔙 вернуться в раздел Нефтесервисные решения': BaseTextMenu.do_nr,
        'История НР': BaseTextMenu.history_nr,

        'Инженерно-технологический сервис': BaseTextMenu.do_its,
        '🔙 вернуться в раздел Инженерно-технологический сервис': BaseTextMenu.do_its,
        'Структура ИТС': BaseTextMenu.structure_its,
        'НМД ИТС': BaseTextMenu.nmd_its,
        'Контакты ИТС': BaseTextMenu.contacts_its,
        'История ИТС': BaseTextMenu.history_its,

        'Газпромнефть Энергосистемы': BaseTextMenu.do_es,
        '🔙 вернуться в раздел Газпромнефть Энергосистемы': BaseTextMenu.do_es,
        'История Энергосистем': BaseTextMenu.history_es,
        'Структура Энергосистем': BaseTextMenu.structure_es,
        'Контакты Энергосистем': BaseTextMenu.contacts_es,

        'Новостная лента': BaseTextMenu.news_feed,
        'Корпоративный портал': BaseTextMenu.corporate_portal,
        'Мобильная лента': BaseTextMenu.mobile_feed,
        'Телеграм-каналы': BaseTextMenu.telegram_channels,

        'Сервисы для сотрудников': BaseTextMenu.services_for_employees,
        '🔙 вернуться в раздел Сервисы': BaseTextMenu.services_for_employees,
        'Сервисы самообслуживания': BaseTextMenu.self_services,
        'Контакт центр': BaseTextMenu.contact_center,

        'Адаптация': BaseTextMenu.adaptation,
        '🔙 вернуться в раздел Адаптация': BaseTextMenu.adaptation,
        'Корпоративная безопасность': BaseTextMenu.corporate_security,
        'Производственная безопасность': BaseTextMenu.industrial_safety,
        'Хоз. и транспорт. обеспечение': BaseTextMenu.economic_and_transport_support,
        'Трудовой распорядок': BaseTextMenu.work_schedule,
        'Внешний вид. Спецодежда и СИЗ': BaseTextMenu.workwear,
        'Мотивация персонала': BaseTextMenu.staff_motivation,
        'Мотивация ЭС': BaseTextMenu.motivation_es,
        'Мотивация НР': BaseTextMenu.motivation_nr,
        'Мотивация ИТС': BaseTextMenu.motivation_its,
        'Мотивация СТ': BaseTextMenu.motivation_st,
        'Буклеты для сотрудников': BaseTextMenu.booklets_for_employees,
        'Книги для сотрудников': BaseTextMenu.books_for_employees,

        'ДМС и РВЛ': BaseTextMenu.dms_and_rvl,
        '🔙 вернуться в раздел ДМС и РВЛ': BaseTextMenu.dms_and_rvl,
        'ДМС': BaseTextMenu.dms,
        'РВЛ': BaseTextMenu.rvl,

        'Карьерное развитие': BaseTextMenu.career_development,
        '🔙 вернуться в раздел Карьерное развитие': BaseTextMenu.career_development,
        'Мой трек': BaseTextMenu.my_track,
        'Мой профиль': BaseTextMenu.my_profile,
        'Индивидуальный план развития': BaseTextMenu.individual_development_plan,
        'Карьерное консультирование': BaseTextMenu.career_counseling,

        'Цикл управления талантами': BaseTextMenu.talent_management_cycle,
        '🔙 вернуться в раздел Цикл управления талантами': BaseTextMenu.talent_management_cycle,
        'Обучение': BaseTextMenu.education,
        'Регулярная оценка': BaseTextMenu.regular_assessment,
        'Диалоги об эффективности': BaseTextMenu.dialogues_about_efficiency,
        'Комитеты по талантам': BaseTextMenu.talent_committees,
        'Диалоги о развитии': BaseTextMenu.development_dialogues,
        'Планирование обучения': BaseTextMenu.planning_education,
        'Комиссия по оценке вклада': BaseTextMenu.contribution_evaluation_commission,

    }

    if message.text in menu_dict.keys():
        menu_dict.get(message.text)(message)

    # СТАЖИРОВКА
    elif (message.text == 'Стажировка' or message.text == '🔙 вернуться в '
          'раздел Стажировка'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('🔙 Главное меню')
        markup.add(button)
        parrent_path = 'prod_data/Стажировка/'
        document_1 = f'{parrent_path}Стажировки_БРД.pdf'
        document_2 = f'{parrent_path}Бланк_плана_стажировки_сотрудника.xlsx'
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
        with (
            open(document_1, 'rb') as file_1,
            open(document_2, 'rb') as file_2,
        ):
            bot.send_document(
                message.chat.id,
                file_1,
                caption='Стажировки БРД',
                parse_mode='html',
            )
            bot.send_document(
                message.chat.id,
                file_2,
                caption='Бланк плана стажировки сотрудника',
                parse_mode='html',
            )

    # ОБУЧЕНИЕ
    elif message.text == 'Полезная литература':
        document = ('prod_data/Обучение/ГПН_ЭС/Почитать/'
                    'электронные_библиотеки.pdf')
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Электронные библиотеки',
                parse_mode="html",
            )

    # ОБУЧЕНИЕ
    elif message.text == 'Цикл планирования обучения':
        document = ('prod_data/Обучение/ГПН_ЭС/'
                    'Целевые_образовательные_программы/educate.pdf')
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Цикл планирования обучения',
                parse_mode="html",
            )

    # ОБУЧЕНИЕ
    elif message.text == 'Каталог программ':
        document = ('prod_data/Обучение/ГПН_ЭС/Каталог_программ/'
                    'Рекомендованные_образовательные_программы.pdf')
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Рекомендованные образовательные программы',
                parse_mode="html",
            )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif (message.text == 'Молодежная политика'
          or message.text == '🔙 вернуться в раздел Молодежная политика'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('🔙 Главное меню')
        button_2 = types.KeyboardButton('Молодежный совет')
        button_3 = types.KeyboardButton('Организация практики')
        button_4 = types.KeyboardButton('Развитие молодых специалистов')
        markup.add(button_2, button_3, button_4, button_1)
        bot.send_message(
            message.from_user.id,
            "Молодежная политика",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif (message.text == 'Организация практики'
          or message.text == '🔙 вернуться в '
                             'раздел Организация практики'):
        document = 'prod_data/Молодежная_политика/org_practics/practis.pdf'
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Прохождение практики в Компании',
                parse_mode="html",
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
        document = (
            'prod_data/Молодежная_политика/MS/'
            'Направления_деятельности/napravlenya.pdf'
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Направления деятельности МС',
                parse_mode="html",
            )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Положение, мотивация МС':
        parrent_path = 'prod_data/Молодежная_политика/MS/Положение_мотивация/'
        file_1 = f'{parrent_path}workorgMS.pdf'
        file_2 = f'{parrent_path}trackMS.pdf'
        file_3 = f'{parrent_path}AnketaMS.docx'
        filename_1 = 'Организация работы Совета молодежи'
        filename_2 = 'Трек вовлеченности МС'
        filename_3 = 'Анкета кандидата'
        files_dict = {
            filename_1: file_1,
            filename_2: file_2,
            filename_3: file_3,
        }
        for caption, document in files_dict.items():
            with open(document, 'rb') as file:
                bot.send_document(
                    message.chat.id,
                    file,
                    caption=caption,
                    parse_mode="html",
                )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Структура МС':
        document = open(
            'prod_data/Молодежная_политика/MS/Структура/structuraMS.pdf',
            'rb',
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
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
        button_3 = types.KeyboardButton('Проект "Моя история успеха"')
        button_4 = types.KeyboardButton(
            '🔙 вернуться в раздел Молодежная политика'
        )
        markup.add(button_1, button_2, button_3, button_4)
        bot.send_message(
            message.from_user.id,
            "Молодежный совет",
            reply_markup=markup,
        )

    # МОЛОДЕЖНАЯ ПОЛИТИКА
    elif message.text == 'Проект "Моя история успеха"':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("перейти в канал",
                   url="https://t.me/podcast_my_success"))
        bot.send_message(
            message.chat.id,
            'Телеграм канал проекта "Моя история успеха"',
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

        file_1 = f'{parrent_path}Заявка_Шаблон.docx'
        file_2 = f'{parrent_path}Шаблон_одностраничника.pptx'
        file_3 = f'{parrent_path}Шаблон_презентации.pptx'
        file_4 = f'{parrent_path}dk.pdf'
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
        for caption, document in files_dict.items():
            with open(document, 'rb') as file:
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

        document = (
            'prod_data/Молодежная_политика/'
            'Развитие_молодых_специалистов/Слет_МС/Слет_МС.pdf'
        )
        with open(document, 'rb') as file:
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
        markup.add(button_1, button_2, button_3, button_4,
                   button_5, button_6, button_7, button_8)
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
        markup.add(button_1, button_2, button_3, button_4, button_5)
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
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(
            message.chat.id,
            'Работа в выходной день',
            reply_markup=markup,
        )

    elif message.text == f'Работа в выходной день {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ES/'
        document = f'{parrent_path}main.docx'
        filename = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=filename,
                parse_mode="html",
            )

    elif message.text == f'Работа в выходной день {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ITS/'
        document = f'{parrent_path}main.docx'
        filename = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=filename,
                parse_mode="html",
            )

    elif message.text == f'Работа в выходной день {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/NNGGF/'
        document = f'{parrent_path}main.docx'
        filename = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=filename,
                parse_mode="html",
            )

    elif message.text == f'Работа в выходной день {NR}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/NR/'
        document = f'{parrent_path}main.docx'
        filename = ('Служебная записка на привлечение к работе '
                    'в выходные дни')
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=filename,
                parse_mode="html",
            )

    elif message.text == f'Работа в выходной день {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/working_day_off/ST/'
        document = f'{parrent_path}main.docx'
        filename = (
            'Ш-14.03.05-15 Решение о привлечении к работе '
            'в выходные нерабоч. праздничные дни или к сверхур.работе'
        )
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=filename,
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
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        with (
            open(f'{parrent_path}SZ.docx', 'rb') as file_1,
            open(f'{parrent_path}list.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode='html',
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode='html',
                    ),
                ]
            )

    elif message.text == f'Простой, задержка в пути {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/ITS/'
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        with (
            open(f'{parrent_path}SZ.docx', 'rb') as file_1,
            open(f'{parrent_path}list.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode='html',
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode='html',
                    ),
                ]
            )

    elif message.text == f'Простой, задержка в пути {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/NNGGF/'
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        with (
            open(f'{parrent_path}SZ.docx', 'rb') as file_1,
            open(f'{parrent_path}list.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode='html',
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode='html',
                    ),
                ]
            )

    elif message.text == f'Простой, задержка в пути {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/delay_in_transit/ST/'
        filename_1 = (
            'Ш-14.03.05-16 Служебная записка о простое /'
            'незапланированном простое, содержащая список работников'
        )
        filename_2 = ('Ш-14.03.05-17 Список работников, которым '
                      'необходимо оформить задержку в пути')
        with (
            open(f'{parrent_path}SZ.docx', 'rb') as file_1,
            open(f'{parrent_path}list.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode='html',
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode='html',
                    ),
                ]
            )

    elif message.text == 'Исполнение гос.обязанностей':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton(f'Исполнение гос.обязанностей {ES}')
        # button_2 = types.KeyboardButton(f'Исполнение гос.обязанностей {NR}')
        button_3 = types.KeyboardButton(f'Исполнение гос.обязанностей {ST}')
        button_4 = types.KeyboardButton(f'Исполнение гос.обязанностей {ITS}')
        button_5 = types.KeyboardButton(
            f'Исполнение гос.обязанностей {NNGGF}'
        )
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
        filename = ('Ш-14.03.05-03 Заявление об исполнении '
                    'государственных или общественных обязанностей')
        with open(f'{parrent_path}main.docx', 'rb') as file:
            bot.send_document(
                    message.chat.id,
                    document=file,
                    caption=filename,
                    parse_mode="html",
                )

    elif message.text == f'Исполнение гос.обязанностей {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/government_duties/ITS/'
        file_name = ('Ш-14.03.05-03 Заявление об исполнении '
                     'государственных или общественных обязанностей')
        with open(f'{parrent_path}main.docx', 'rb') as file:
            bot.send_document(
                    message.chat.id,
                    document=file,
                    caption=file_name,
                    parse_mode="html",
                )

    elif message.text == f'Исполнение гос.обязанностей {NNGGF}':
        parrent_path = ('prod_data/blanks/time_tracking/government_duties/'
                        'NNGGF/')
        file_name = ('Ш-14.03.05-03 Заявление об исполнении '
                     'государственных или общественных обязанностей')
        with open(f'{parrent_path}main.docx', 'rb') as file:
            bot.send_document(
                    message.chat.id,
                    document=file,
                    caption=file_name,
                    parse_mode="html",
                )

    elif message.text == f'Исполнение гос.обязанностей {ST}':
        parrent_path = ('prod_data/blanks/time_tracking/government_duties/ST/')
        file_name = ('Ш-14.03.05-03 Заявление об исполнении '
                     'государственных или общественных обязанностей')
        with open(f'{parrent_path}main.docx', 'rb') as file:
            bot.send_document(
                    message.chat.id,
                    document=file,
                    caption=file_name,
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
            'Изменение графика работы',
            reply_markup=markup,
        )

    elif message.text == f'Изменение графика {ES}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ES/'
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        with (
            open(f'{parrent_path}main.docx', 'rb') as file_1,
            open(f'{parrent_path}baby_cancel.docx', 'rb') as file_2,
            open(f'{parrent_path}change.docx', 'rb') as file_3,
            open(f'{parrent_path}new.docx', 'rb') as file_4,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_4,
                        caption=filename_4,
                        parse_mode="html",
                    ),
                ]
            )

    elif message.text == f'Изменение графика {ITS}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ITS/'
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        with (
            open(f'{parrent_path}main.docx', 'rb') as file_1,
            open(f'{parrent_path}baby_cancel.docx', 'rb') as file_2,
            open(f'{parrent_path}change.docx', 'rb') as file_3,
            open(f'{parrent_path}new.docx', 'rb') as file_4,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_4,
                        caption=filename_4,
                        parse_mode="html",
                    ),
                ]
            )

    elif message.text == f'Изменение графика {NNGGF}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/NNGGF/'
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_3 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        with (
            open(f'{parrent_path}main.docx', 'rb') as file_1,
            open(f'{parrent_path}change.docx', 'rb') as file_2,
            open(f'{parrent_path}new.docx', 'rb') as file_3,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                ]
            )

    elif message.text == f'Изменение графика {NR}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/NR/'
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.02-03 Заявление об изменении '
                      'режима рабочего времени')
        with (
            open(f'{parrent_path}main.docx', 'rb') as file_1,
            open(f'{parrent_path}change_grafik.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                ]
            )

    elif message.text == f'Изменение графика {ST}':
        parrent_path = 'prod_data/blanks/time_tracking/change_shedule/ST/'
        filename_1 = ('Ш-14.03.05-02 Заявление об изменении '
                      'графика работы персонала')
        filename_2 = ('Ш-14.03.05-04 Заявление о досрочном выходе '
                      'из отпуска по уходу за ребенком')
        filename_3 = ('Ш-14.03.05-13 Служебная записка об изменении '
                      'графика работы персонала')
        filename_4 = ('Ш-14.03.05-14 Служебная записка о необходимости '
                      'формирования нового графика работы персонала')
        with (
            open(f'{parrent_path}main.docx', 'rb') as file_1,
            open(f'{parrent_path}baby_cancel.docx', 'rb') as file_2,
            open(f'{parrent_path}change.docx', 'rb') as file_3,
            open(f'{parrent_path}new.docx', 'rb') as file_4,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_4,
                        caption=filename_4,
                        parse_mode="html",
                    ),
                ]
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
        with (
            open(f'{parrent_path}rodi.doc', 'rb') as file_1,
            open(f'{parrent_path}ranie_rodi.doc', 'rb') as file_2,
            open(f'{parrent_path}posobie_3.doc', 'rb') as file_3,
            open(f'{parrent_path}premia.doc', 'rb') as file_4,
            open(f'{parrent_path}posobie_1.5.doc', 'rb') as file_5,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_4,
                        caption=filename_4,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_5,
                        caption=filename_5,
                        parse_mode="html",
                    ),
                ]
            )

    elif message.text == f'Рождение ребенка {ITS}':
        parrent_path = 'prod_data/blanks/baby_born/ITS/'
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
        with (
            open(f'{parrent_path}rodi.doc', 'rb') as file_1,
            open(f'{parrent_path}ranie_rodi.doc', 'rb') as file_2,
            open(f'{parrent_path}posobie_3.doc', 'rb') as file_3,
            open(f'{parrent_path}premia.doc', 'rb') as file_4,
            open(f'{parrent_path}posobie_1.5.doc', 'rb') as file_5,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_4,
                        caption=filename_4,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_5,
                        caption=filename_5,
                        parse_mode="html",
                    ),
                ]
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
            'Отмена, отзыв из отпуска.',
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
        button_1 = types.KeyboardButton(f'Бланки {ES}')
        button_2 = types.KeyboardButton(f'Бланки {NR}')
        button_3 = types.KeyboardButton(f'Бланки {ST}')
        button_4 = types.KeyboardButton(f'Бланки {ITS}')
        button_5 = types.KeyboardButton(f'Бланки {NNGGF}')
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

    elif message.text == f'Бланки {ES}':
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

    elif message.text == f'Бланки {NR}':
        parrent_path = 'prod_data/blanks/avansov/NR/'
        file_1 = open(f'{parrent_path}SOP.pdf', 'rb')
        filename_1 = 'СОП по оформлению отчета по командировке с 01.10.23'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Бланки {ITS}':
        parrent_path = 'prod_data/blanks/avansov/ITS/'
        file_1 = open(f'{parrent_path}blank_1.xls', 'rb')
        filename_1 = 'Бланк авансового отчета'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Бланки {NNGGF}':
        parrent_path = 'prod_data/blanks/avansov/ITS/'
        file_1 = open(f'{parrent_path}blank_2.xls', 'rb')
        filename_1 = 'Бланк авансового отчета'
        bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
        )

    elif message.text == f'Бланки {ST}':
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

    # ЗАКУПКИ
    elif (message.text == 'Планирование закупок'
          or message.text == '🔙 вернуться в раздел закупок'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button_1 = types.KeyboardButton('Закупки у СМиСП')
        button_2 = types.KeyboardButton('Код услуги')
        button_3 = types.KeyboardButton('Комплект документов для закупки')
        button_4 = types.KeyboardButton('Корректировки ГПЗ')
        button_5 = types.KeyboardButton('Обоснование закупки')
        button_6 = types.KeyboardButton('🔙 Главное меню')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        parrent_path = 'prod_data/zakupki/'
        document = f'{parrent_path}planing_info.pdf'
        bot.send_message(
            message.from_user.id,
            "Планирование закупок",
            reply_markup=markup
        )
        if message.text == 'Планирование закупок':
            with open(document, 'rb') as file:
                bot.send_document(
                    message.chat.id,
                    file,
                    caption='Памятка Инициатора по планированию закупок',
                    parse_mode="html",
                )

    # ЗАКУПКИ
    elif message.text == 'Закупки у СМиСП':
        parrent_path = 'prod_data/zakupki/SM_and_SP/'
        document = f'{parrent_path}SM_SP_list.xlsx'
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Перечень закупок у СМиСП ред. 5 от 07.02.2020г.',
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Код услуги':
        parrent_path = 'prod_data/zakupki/code_uslugi/'
        document = f'{parrent_path}code_KT_777.xlsx'
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Код услуги КТ-777',
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Корректировки ГПЗ':
        parrent_path = 'prod_data/zakupki/GPZ_correct/'
        filename_1 = 'Шаблон корректировки ГПЗ (Образец)'
        filename_2 = 'Шаблон корректировки ГПЗ'
        with (
            open(f'{parrent_path}tamplate_sample.xlsx', 'rb') as file_1,
            open(f'{parrent_path}template.xlsx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                ]
            )

    # ЗАКУПКИ
    elif message.text == 'Обоснование закупки':
        parrent_path = 'prod_data/zakupki/zakupka_rationale/'
        document = f'{parrent_path}justification.xlsx'
        with open(document, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption='Обоснование закупки',
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Комплект документов для закупки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button_1 = types.KeyboardButton('Безальтернативная закупка')
        button_2 = types.KeyboardButton('Закупка ВЗЛ')
        button_3 = types.KeyboardButton('Закупка у единственного поставщика')
        button_4 = types.KeyboardButton('Конкурентный отбор')
        button_5 = types.KeyboardButton('Расчет НМЦ')
        button_6 = types.KeyboardButton('🔙 вернуться в раздел закупок')
        markup.add(
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
        )
        bot.send_message(
            message.from_user.id,
            "Комплект документов для закупки",
            reply_markup=markup
        )

    # ЗАКУПКИ
    elif message.text == 'Безальтернативная закупка':
        parrent_path = 'prod_data/zakupki/zakupka_docs/bez_alternative/'
        filename_1 = '1. Реестр БАЗ'
        filename_2 = '2. Техническое задание'
        with (
            open(f'{parrent_path}bd_catalog.xlsx', 'rb') as file_1,
            open(f'{parrent_path}tz.docx', 'rb') as file_2,
        ):
            bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )
            bot.send_document(
                message.chat.id,
                document=file_2,
                caption=filename_2,
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Закупка ВЗЛ':
        parrent_path = 'prod_data/zakupki/zakupka_docs/VZL/'
        filename_1 = '1. Расчет НМЦ (Прочий метод)'
        filename_2 = '2. Техническое задание'
        filename_3 = '3. Пояснение к закупке ВЗЛ'
        with (
            open(f'{parrent_path}calc_nmc_info.xlsx', 'rb') as file_1,
            open(f'{parrent_path}info_vzl.docx', 'rb') as file_2,
            open(f'{parrent_path}tz_vzl.docx', 'rb') as file_3,
        ):
            bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )
            bot.send_document(
                message.chat.id,
                document=file_2,
                caption=filename_2,
                parse_mode="html",
            )
            bot.send_document(
                message.chat.id,
                document=file_3,
                caption=filename_3,
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Закупка у единственного поставщика':
        parrent_path = 'prod_data/zakupki/zakupka_docs/one_postav/'
        filename_1 = '1. Техническое задание'
        filename_2 = '2. Заключение по итогам анализа рынка'
        with (
            open(f'{parrent_path}tz_one_person.docx', 'rb') as file_1,
            open(f'{parrent_path}analitics_info.docx', 'rb') as file_2,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                ]
            )

    # ЗАКУПКИ
    elif message.text == 'Конкурентный отбор':
        parrent_path = 'prod_data/zakupki/zakupka_docs/concurent/'
        filename_1 = '1. Техническое задание'
        filename_2 = '2. Обоснование ЗКО'
        with (
            open(f'{parrent_path}tz_concurent.docx', 'rb') as file_1,
            open(f'{parrent_path}ZKO_info.pdf', 'rb') as file_2,
        ):
            bot.send_document(
                message.chat.id,
                document=file_1,
                caption=filename_1,
                parse_mode="html",
            )
            bot.send_document(
                message.chat.id,
                document=file_2,
                caption=filename_2,
                parse_mode="html",
            )

    # ЗАКУПКИ
    elif message.text == 'Расчет НМЦ':
        parrent_path = 'prod_data/zakupki/zakupka_docs/calc_NMC/'
        filename_1 = 'Шаблон №1. Расчет НМЦ (затратный метод)'
        filename_2 = 'Шаблон №2. Расчет НМЦ (метод сопоставимых рыночных цен)'
        filename_3 = 'Шаблон №3. Расчет НМЦ (тарифный метод)'
        with (
            open(f'{parrent_path}calc_zatrat.xlsx', 'rb') as file_1,
            open(f'{parrent_path}calc_rinok.xlsx', 'rb') as file_2,
            open(f'{parrent_path}calc_tarif.xlsx', 'rb') as file_3,
        ):
            bot.send_media_group(
                message.chat.id,
                [
                    telebot.types.InputMediaDocument(
                        file_1,
                        caption=filename_1,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_2,
                        caption=filename_2,
                        parse_mode="html",
                    ),
                    telebot.types.InputMediaDocument(
                        file_3,
                        caption=filename_3,
                        parse_mode="html",
                    ),
                ]
            )

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
def user_photo(message: telebot.types.Message):
    """Ловим отправленные пользователем изобращения."""
    BaseContentProcessor.get_user_photo(message)


@bot.message_handler(content_types=['sticker'])
def user_stiсker(message: telebot.types.Message):
    """Ловим отправленные пользователем стикеры."""
    BaseContentProcessor.get_user_stiсker(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
