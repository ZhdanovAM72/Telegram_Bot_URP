from typing import Callable

from telebot import types
from bot.utils.buttons import Buttons
from bot import bot

FAQ = """
    ИПР:
    \n1. Как внести изменения в свой ИПР, если он уже согласован?
    \n2. Кем я могу стать, как мне повысить должность?
"""
FAQ_2 = """
    Проблемы со входом на портал/ИПР для сотрудников ИТС- что делать?
    \n1. У меня нет доступа к Карьерному порталу/Порталу знаний? 
    \n2. У меня не верно указан линейный руководитель на Карьерном портале, я не могу направить на согласование свой ИПР.
    \n3. У меня был заполнен профиль/ИПР, а сейчас 0%.
"""


class FAQService:

    @staticmethod
    def faq_service_main(message: types.Message) -> types.Message:
        buttons = (
            (
                "1. изменения",
                "ИПР_1",
            ),
            (
                "2. должность",
                "ИПР_2",
            ),
        )
        markup = Buttons.create_inline_keyboard(buttons, row_width=2, callback=True)
        bot.send_message(
            message.chat.id,
            text=f"{FAQ}",
            reply_markup=markup,
            parse_mode="html",
        )
        buttons = (
            (
                "1. доступ",
                "портал/ИПР_1",
            ),
            (
                "2. ошибка",
                "портал/ИПР_2",
            ),
            (
                "3. заполнение",
                "портал/ИПР_3",
            ),
        )
        markup = Buttons.create_inline_keyboard(buttons, row_width=1, callback=True)
        bot.send_message(
            message.chat.id,
            text=f"{FAQ_2}",
            reply_markup=markup,
            parse_mode="html",
        )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data == 'ИПР_1')
    def ipr_1(call: Callable[[types.Message], None]) -> types.Message:
        return bot.send_message(
            call.message.chat.id,
            text='Необходимо перевести ИПР в статус "Разработка". Это можно сделать путем нажатия кнопки "Редактировать" долгосрочную цель. После этого можно вносить изменения в ИПР. ',
            parse_mode="html",
        )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data == 'ИПР_2')
    def ipr_2(call: Callable[[types.Message], None]) -> types.Message:
        return bot.send_message(
            call.message.chat.id,
            text='Свои карьерные ожидания Вы можете обсудить во время диалога об эффективности. В профиле на Карьерном портале укажите интересующую целевую роль. Помощь в определении вектора развития Вы можете получить у линейного и/или функционального руководителя, или у карьерного консультанта. Каждому работнику доступно 5 консультаций в год. Записаться можно на Карьерном портале.',
            parse_mode="html",
        )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data == 'портал/ИПР_1')
    def portal_1(call: Callable[[types.Message], None]) -> types.Message:
        return bot.send_message(
            call.message.chat.id,
            text='Из-за миграции персонала из ННГГФ в ИТС в информационной базе КСУ НСИ ПД (ЕССТ) две карточки по сотруднику, одна из карточек заблокирована, содержит дату увольнения и блокировку, вторая полностью опубликована, логин и почта переданы. Но интеграция web tutor работает не только с карточкой сотрудника ЕССТ, но и с карточкой консолидации SAP, но в базе такая только одна, по активной карточке сотрудника. Потому что источником данных заблокированной карточки сотрудника является AD. Получается что нет заблокированной, с датой увольнения карточки из SAP, следовательно данная информация не уходит. SAP HR в свою очередь не сможет сделать карточку сотрудника консолидации по уже ранее уволенному сотруднику, который ввелся в AD. ИТС не находится в периметре поддержки SAP HR и консолидации 1С ЗУП. Вы можете оставить обращение по восстановлению доступа на Портале самообслуживания.',
            parse_mode="html",
        )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data == 'портал/ИПР_2')
    def portal_2(call: Callable[[types.Message], None]) -> types.Message:
        return bot.send_message(
            call.message.chat.id,
            text='Из-за миграции персонала из ННГГФ в ИТС и устаревшей версии кадровых систем наблюдаются сбои в организационной структуре Обществ. Вы можете оставить обращение по актуализации линейного руководителя на Портале самообслуживания. ',
            parse_mode="html",
        )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: call.data == 'портал/ИПР_3')
    def portal_3(call: Callable[[types.Message], None]) -> types.Message:
        return bot.send_message(
            call.message.chat.id,
            text='Из-за миграции персонала из ННГГФ в ИТС в информационной базе КСУ НСИ ПД (ЕССТ) две карточки по сотруднику, одна из карточек заблокирована, содержит дату увольнения и блокировку, вторая полностью опубликована, логин и почта переданы. Но интеграция web tutor работает не только с карточкой сотрудника ЕССТ, но и с карточкой консолидации SAP, но в базе такая только одна, по активной карточке сотрудника. Потому что источником данных заблокированной карточки сотрудника является AD. Получается что нет заблокированной, с датой увольнения карточки из SAP, следовательно данная информация не уходит. SAP HR в свою очередь не сможет сделать карточку сотрудника консолидации по уже ранее уволенному сотруднику, который ввелся в AD. ИТС не находится в периметре поддержки SAP HR и консолидации 1С ЗУП. Вы можете оставить обращение по восстановлению профиля/ИПР на Портале самообслуживания. ',
            parse_mode="html",
        )
