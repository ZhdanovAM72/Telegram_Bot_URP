import telebot
from telebot import types

from bot.bot_command import BaseBotCommands
from bot.content_processor import BaseContentProcessor
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command, log_user_command_updated, logger
from bot.constants import (
    ES, ITS, NR, NNGGF, ST,
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


@bot.message_handler(
    commands=[
        'deleteuser',
        'deletecode',
    ]
)
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
        'createcode_ITS',
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


@bot.message_handler(
    commands=[
        'updates',
        'massmess',
    ]
)
def mass_info_message(message: types.Message) -> types.Message | None:
    """
    Рассылка информации всем пользователям.
    - updates: для заготовленных обновлений
    - massmess: для любых сообщений (до 500 символов)
    """
    BaseBotCommands.mass_info_message(message)


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

        # О КОМПАНИИ
        'О компании': BaseTextMenu.about_company,
        '🔙 вернуться в раздел О компании': BaseTextMenu.about_company,
        'Корпоративные ценности': BaseTextMenu.corporate_values,
        'Выбрать ДО': BaseTextMenu.choose_do,
        '🔙 вернуться в раздел Выбрать ДО': BaseTextMenu.choose_do,

        # СТ
        'Газпромнефть Сервисные технологии': BaseTextMenu.do_st,
        '🔙 вернуться в раздел Газпромнефть Сервисные технологии': BaseTextMenu.do_st,
        'Структура СТ': BaseTextMenu.structure_st,
        'История СТ': BaseTextMenu.history_st,

        # НР
        'Нефтесервисные решения': BaseTextMenu.do_nr,
        '🔙 вернуться в раздел Нефтесервисные решения': BaseTextMenu.do_nr,
        'История НР': BaseTextMenu.history_nr,

        # ИТС
        'Инженерно-технологический сервис': BaseTextMenu.do_its,
        '🔙 вернуться в раздел Инженерно-технологический сервис': BaseTextMenu.do_its,
        'Структура ИТС': BaseTextMenu.structure_its,
        'НМД ИТС': BaseTextMenu.nmd_its,
        'Контакты ИТС': BaseTextMenu.contacts_its,
        'История ИТС': BaseTextMenu.history_its,

        # ЭНЕРГОСИСТЕМЫ
        'Газпромнефть Энергосистемы': BaseTextMenu.do_es,
        '🔙 вернуться в раздел Газпромнефть Энергосистемы': BaseTextMenu.do_es,
        'История Энергосистем': BaseTextMenu.history_es,
        'Структура Энергосистем': BaseTextMenu.structure_es,
        'Контакты Энергосистем': BaseTextMenu.contacts_es,

        # НОВОСТНАЯ ЛЕНТА
        'Новостная лента': BaseTextMenu.news_feed,
        'Корпоративный портал': BaseTextMenu.corporate_portal,
        'Мобильная лента': BaseTextMenu.mobile_feed,
        'Телеграм-каналы': BaseTextMenu.telegram_channels,

        # СЕРВИСЫ ДЛЯ СОТРУДНИКОВ
        'Сервисы для сотрудников': BaseTextMenu.services_for_employees,
        '🔙 вернуться в раздел Сервисы': BaseTextMenu.services_for_employees,
        'Сервисы самообслуживания': BaseTextMenu.self_services,
        'Контакт центр': BaseTextMenu.contact_center,

        # АДАПТАЦИЯ
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

        # ДМС и РВЛ
        'ДМС и РВЛ': BaseTextMenu.dms_and_rvl,
        '🔙 вернуться в раздел ДМС и РВЛ': BaseTextMenu.dms_and_rvl,
        'ДМС': BaseTextMenu.dms,
        'РВЛ': BaseTextMenu.rvl,

        # КАРЬЕРНОЕ РАЗВИТИЕ
        'Карьерное развитие': BaseTextMenu.career_development,
        '🔙 вернуться в раздел Карьерное развитие': BaseTextMenu.career_development,
        'Мой трек': BaseTextMenu.my_track,
        'Мой профиль': BaseTextMenu.my_profile,
        'Индивидуальный план развития': BaseTextMenu.individual_development_plan,
        'Карьерное консультирование': BaseTextMenu.career_counseling,

        # ЦИКЛ УПРАВЛЕНИЯ ТАЛАНТАМИ
        'Цикл управления талантами': BaseTextMenu.talent_management_cycle,
        '🔙 вернуться в раздел Цикл управления талантами': BaseTextMenu.talent_management_cycle,
        'Регулярная оценка': BaseTextMenu.regular_assessment,
        'Диалоги об эффективности': BaseTextMenu.dialogues_about_efficiency,
        'Комитеты по талантам': BaseTextMenu.talent_committees,
        'Диалоги о развитии': BaseTextMenu.development_dialogues,
        'Комиссия по оценке вклада': BaseTextMenu.contribution_evaluation_commission,

        # ОБУЧЕНИЕ
        'Обучение': BaseTextMenu.education,
        'Планирование обучения': BaseTextMenu.planning_education,
        'Полезная литература': BaseTextMenu.useful_literature,
        'Цикл планирования обучения': BaseTextMenu.training_planning_cycle,
        'Каталог программ': BaseTextMenu.program_catalog,

        # СТАЖИРОВКА
        'Стажировка': BaseTextMenu.internship,

        # МОЛОДЕЖНАЯ ПОЛИТИКА
        'Молодежная политика': BaseTextMenu.youth_policy,
        '🔙 вернуться в раздел Молодежная политика': BaseTextMenu.youth_policy,
        'Организация практики': BaseTextMenu.organization_of_practice,
        'Молодежный совет': BaseTextMenu.youth_council,
        '🔙 вернуться в раздел Молодежный совет': BaseTextMenu.youth_council,
        'Направления деятельности МС': BaseTextMenu.youth_council_activity,
        'Положение, мотивация МС': BaseTextMenu.youth_council_documents,
        'Структура МС': BaseTextMenu.youth_council_structure,
        'Развитие молодых специалистов': BaseTextMenu.youth_council_development,
        'Проект "Моя история успеха"': BaseTextMenu.my_success_story,
        'НТК МС': BaseTextMenu.scientific_technical_conference,
        'СЛЕТ МС': BaseTextMenu.youth_council_meeting,

        # БЛАНКИ ЗАЯВЛЕНИЙ
        'Бланки заявлений': BaseTextMenu.application_forms_main,
        '🔙 вернуться в раздел Бланки заявлений': BaseTextMenu.application_forms_main,

        # АВАНСОВЫЙ ОТЧЕТ
        'Авансовый отчет': BaseTextMenu.advance_report,
        f'Бланки {ES}': BaseTextMenu.forms_es,
        f'Бланки {NR}': BaseTextMenu.forms_nr,
        f'Бланки {ST}': BaseTextMenu.forms_st,
        f'Бланки {ITS}': BaseTextMenu.forms_its,
        f'Бланки {NNGGF}': BaseTextMenu.forms_nnggf,

        # БАНКОВСКИЕ РЕКВИЗИТЫ
        'Банковские реквизиты': BaseTextMenu.bank_details_main,
        f'Банковские реквизиты {ES}': BaseTextMenu.bank_details_es,
        f'Банковские реквизиты {NR}': BaseTextMenu.bank_details_nr,
        f'Банковские реквизиты {ST}': BaseTextMenu.bank_details_st,
        f'Банковские реквизиты {ITS}': BaseTextMenu.bank_details_its,
        f'Банковские реквизиты {NNGGF}': BaseTextMenu.bank_details_nnggf,

        'Изменение трудового договора': BaseTextMenu.change_employment_contract,
        "🔙 вернуться в раздел Изменение трудового договора": BaseTextMenu.change_employment_contract,

        # ДОПОЛНИТЕЛЬНАЯ РАБОТА
        "Дополнительная работа": BaseTextMenu.extra_work_main,
        f'Доп. работа {ES}': BaseTextMenu.extra_work_es,
        f'Доп. работа {NR}': BaseTextMenu.extra_work_nr,
        f'Доп. работа {ST}': BaseTextMenu.extra_work_st,
        f'Доп. работа {ITS}': BaseTextMenu.extra_work_its,
        f'Доп. работа {NNGGF}': BaseTextMenu.extra_work_nnggf,

        # ПЕРЕВОДЫ
        "Переводы": BaseTextMenu.transfers_main,
        f'Переводы {ES}': BaseTextMenu.transfers_es,
        f'Переводы {NR}': BaseTextMenu.transfers_nr,
        f'Переводы {ST}': BaseTextMenu.transfers_st,
        f'Переводы {ITS}': BaseTextMenu.transfers_its,
        f'Переводы {NNGGF}': BaseTextMenu.transfers_nnggf,


        # РЕЖИМ РАБОЧЕГО ВРЕМЕНИ
        "Режим рабочего времени": BaseTextMenu.working_hours_main,
        f'Режим рабочего времени {ES}': BaseTextMenu.working_hours_es,
        f'Режим рабочего времени {NR}': BaseTextMenu.working_hours_nr,
        f'Режим рабочего времени {ST}': BaseTextMenu.working_hours_st,
        f'Режим рабочего времени {ITS}': BaseTextMenu.working_hours_its,
        f'Режим рабочего времени {NNGGF}': BaseTextMenu.working_hours_nnggf,

        # ОФОРМЛЕНИЕ ОТПУСКОВ
        'Оформление отпусков': BaseTextMenu.vacation_registration_main,
        '🔙 вернуться в раздел Оформление отпусков': BaseTextMenu.vacation_registration_main,

        # ДРУГИЕ ВИДЫ ОТПУСКОВ
        'Другие виды отпусков': BaseTextMenu.other_types_vacation_main,
        f'Другие виды отпусков {ES}': BaseTextMenu.other_types_vacation_es,
        f'Другие виды отпусков {NR}': BaseTextMenu.other_types_vacation_nr,
        f'Другие виды отпусков {ST}': BaseTextMenu.other_types_vacation_st,
        f'Другие виды отпусков {ITS}': BaseTextMenu.other_types_vacation_its,
        f'Другие виды отпусков {NNGGF}': BaseTextMenu.other_types_vacation_nnggf,

        # ОТМЕНА, ОТЗЫВ ИЗ ОТПУСКА
        'Отмена, отзыв из отпуска': BaseTextMenu.cancellation_recall_vacation_main,
        f'Отмена, отзыв из отпуска {ES}': BaseTextMenu.cancellation_recall_vacation_es,
        f'Отмена, отзыв из отпуска {NR}': BaseTextMenu.cancellation_recall_vacation_nr,
        f'Отмена, отзыв из отпуска {ST}': BaseTextMenu.cancellation_recall_vacation_st,
        f'Отмена, отзыв из отпуска {ITS}': BaseTextMenu.cancellation_recall_vacation_its,
        f'Отмена, отзыв из отпуска {NNGGF}': BaseTextMenu.cancellation_recall_vacation_nnggf,

        # ОТПУСК БЕЗ СОХРАНЕНИЯ ЗП
        'Отпуск без сохранения зп': BaseTextMenu.vacation_without_pay_main,
        f'Отпуск без сохранения зп {ES}': BaseTextMenu.vacation_without_pay_es,
        f'Отпуск без сохранения зп {NR}': BaseTextMenu.vacation_without_pay_nr,
        f'Отпуск без сохранения зп {ST}': BaseTextMenu.vacation_without_pay_st,
        f'Отпуск без сохранения зп {ITS}': BaseTextMenu.vacation_without_pay_its,
        f'Отпуск без сохранения зп {NNGGF}': BaseTextMenu.vacation_without_pay_nnggf,

        # ПЕРЕНОС, ПРОДЛЕНИЕ ОТПУСКА
        'Перенос, продление отпуска': BaseTextMenu.transfer_extension_vacation_main,
        f'Перенос, продление отпуска {ES}': BaseTextMenu.transfer_extension_vacation_es,
        f'Перенос, продление отпуска {NR}': BaseTextMenu.transfer_extension_vacation_nr,
        f'Перенос, продление отпуска {ST}': BaseTextMenu.transfer_extension_vacation_st,
        f'Перенос, продление отпуска {ITS}': BaseTextMenu.transfer_extension_vacation_its,
        f'Перенос, продление отпуска {NNGGF}': BaseTextMenu.transfer_extension_vacation_nnggf,


        # СДАЧА КРОВИ
        'Сдача крови': BaseTextMenu.blood_donation_main,
        f'Сдача крови {ES}': BaseTextMenu.blood_donation_es,
        f'Сдача крови {NR}': BaseTextMenu.blood_donation_nr,
        f'Сдача крови {ST}': BaseTextMenu.blood_donation_st,
        f'Сдача крови {ITS}': BaseTextMenu.blood_donation_its,
        f'Сдача крови {NNGGF}': BaseTextMenu.blood_donation_nnggf,

        # ПРЕКРАЩЕНИЕ ТРУДОВОГО ДОГОВОРА
        'Прекращение трудового договора': BaseTextMenu.termination_contract_main,
        f'Прекращение ТД {ES}': BaseTextMenu.termination_contract_es,
        f'Прекращение ТД {NR}': BaseTextMenu.termination_contract_nr,
        f'Прекращение ТД {ST}': BaseTextMenu.termination_contract_its,
        f'Прекращение ТД {ITS}': BaseTextMenu.termination_contract_st,
        f'Прекращение ТД {NNGGF}': BaseTextMenu.termination_contract_nnggf,

        # РОЖДЕНИЕ РЕБЕНКА
        'Рождение ребенка': BaseTextMenu.birth_child_main,
        f'Рождение ребенка {ES}': BaseTextMenu.birth_child_es,
        f'Рождение ребенка {NR}': BaseTextMenu.birth_child_nr,
        f'Рождение ребенка {ST}': BaseTextMenu.birth_child_st,
        f'Рождение ребенка {ITS}': BaseTextMenu.birth_child_its,
        f'Рождение ребенка {NNGGF}': BaseTextMenu.birth_child_nnggf,

        # УЧЕТ РАБОЧЕГО ВРЕМЕНИ
        'Учет рабочего времени': BaseTextMenu.time_tracking,
        '🔙 вернуться в раздел Учет рабочего времени': BaseTextMenu.time_tracking,
        # ИЗМЕНЕНИЕ ГРАФИКА РАБОТЫ
        'Изменение графика работы': BaseTextMenu.work_schedule_main,
        f'Изменение графика {ES}': BaseTextMenu.change_schedule_es,
        f'Изменение графика {NR}': BaseTextMenu.change_schedule_nr,
        f'Изменение графика {ST}': BaseTextMenu.change_schedule_st,
        f'Изменение графика {ITS}': BaseTextMenu.change_schedule_its,
        f'Изменение графика {NNGGF}': BaseTextMenu.change_schedule_nnggf,

        # ИСПОЛНЕНИЕ ГОС.ОБЯЗАННОСТЕЙ
        'Исполнение гос.обязанностей': BaseTextMenu.government_duties_main,
        f'Исполнение гос.обязанностей {ES}': BaseTextMenu.government_duties_es,
        f'Исполнение гос.обязанностей {ST}': BaseTextMenu.government_duties_st,
        f'Исполнение гос.обязанностей {ITS}': BaseTextMenu.government_duties_its,
        f'Исполнение гос.обязанностей {NNGGF}': BaseTextMenu.government_duties_nnggf,

        # ПРОСТОЙ, ЗАДЕРЖКА В ПУТИ
        'Простой, задержка в пути': BaseTextMenu.delay_it_transit_main,
        f'Простой, задержка в пути {ES}': BaseTextMenu.delay_it_transit_es,
        f'Простой, задержка в пути {ST}': BaseTextMenu.delay_it_transit_st,
        f'Простой, задержка в пути {ITS}': BaseTextMenu.delay_it_transit_its,
        f'Простой, задержка в пути {NNGGF}': BaseTextMenu.delay_it_transit_nnggf,

        # РАБОТА В ВЫХОДНОЙ ДЕНЬ
        'Работа в выходной день': BaseTextMenu.day_off_working_main,
        f'Работа в выходной день {ES}': BaseTextMenu.day_off_working_es,
        f'Работа в выходной день {NR}': BaseTextMenu.day_off_working_nr,
        f'Работа в выходной день {ST}': BaseTextMenu.day_off_working_st,
        f'Работа в выходной день {ITS}': BaseTextMenu.day_off_working_its,
        f'Работа в выходной день {NNGGF}': BaseTextMenu.day_off_working_nnggf,

    }

    if message.text in menu_dict.keys():
        menu_dict.get(message.text)(message)

    # ОБРАТНАЯ СВЯЗЬ
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
    logger.info(log_user_command_updated(message))
    return log_user_command(message)


@bot.message_handler(content_types=['photo'])
def user_photo(message: telebot.types.Message):
    """Ловим отправленные пользователем изобращения."""
    return BaseContentProcessor.get_user_photo(message)


@bot.message_handler(content_types=['sticker'])
def user_stiсker(message: telebot.types.Message):
    """Ловим отправленные пользователем стикеры."""
    return BaseContentProcessor.get_user_stiсker(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
