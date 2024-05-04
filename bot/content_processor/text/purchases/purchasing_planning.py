from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot

PARRENT_PATH = "prod_data/zakupki/"


class PurchasingPlanning:

    @staticmethod
    def purchasing_planning_menu(message: types.Message) -> types.Message:
        buttons = (
            'Закупки у СМиСП',
            'Код услуги',
            'Комплект документов для закупки',
            'Корректировки ГПЗ',
            'Обоснование закупки',
            '🔙 Главное меню',
        )
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ Планирование закупок",
            reply_markup=markup,
        )
        if message.text == 'Планирование закупок':
            document = (f"{PARRENT_PATH}planing_info.pdf",)
            caption = ("Памятка Инициатора по планированию закупок",)
            Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def purchases_smisp(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}SM_and_SP/SM_SP_list.xlsx",)
        caption = ("Перечень закупок у СМиСП ред. 5 от 07.02.2020г.",)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def code_uslugi(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}code_uslugi/code_KT_777.xlsx",)
        caption = ("Код услуги КТ-777",)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    @contextmanager
    def gpz_correct(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}GPZ_correct/tamplate_sample.xlsx", "rb"),
                "caption": "Шаблон корректировки ГПЗ (Образец)",
            },
            {
                "file": open(f"{PARRENT_PATH}GPZ_correct/template.xlsx", "rb"),
                "caption": "Шаблон корректировки ГПЗ",
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    def zakupka_rationale(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}zakupka_rationale/justification.xlsx",)
        caption = ("Обоснование закупки",)
        Documents.send_document_with_markup(message.chat.id, document, caption)
