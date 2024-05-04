from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot

PARRENT_PATH = "prod_data/zakupki/zakupka_docs/"


class PurchasingDocuments:

    @staticmethod
    def purchasing_documents_menu(message: types.Message) -> types.Message:
        buttons = (
            'Безальтернативная закупка',
            'Закупка ВЗЛ',
            'Закупка у единственного поставщика',
            'Конкурентный отбор',
            'Расчет НМЦ',
            '🔙 вернуться в раздел закупок',
        )
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.from_user.id,
            text="⬇ Комплект документов для закупки",
            reply_markup=markup,
        )

    @staticmethod
    def no_alternative_purchase(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}bez_alternative/bd_catalog.xlsx",
            f"{PARRENT_PATH}bez_alternative/tz.docx",
        )
        captions = (
            "1. Реестр БАЗ",
            "2. Техническое задание",
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def purchase_vzl(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}VZL/calc_nmc_info.xlsx",
            f"{PARRENT_PATH}VZL/info_vzl.docx",
            f"{PARRENT_PATH}VZL/tz_vzl.docx",
        )
        captions = (
            "1. Расчет НМЦ (Прочий метод)",
            "2. Техническое задание",
            "3. Пояснение к закупке ВЗЛ",
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    @contextmanager
    def purchasing_single_supplier(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}one_postav/tz_one_person.docx", "rb"),
                "caption": "1. Техническое задание",
            },
            {
                "file": open(f"{PARRENT_PATH}one_postav/analitics_info.docx", "rb"),
                "caption": "2. Заключение по итогам анализа рынка",
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    def competitive_selection(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}concurent/tz_concurent.docx",
            f"{PARRENT_PATH}concurent/ZKO_info.pdf",
        )
        captions = (
            "1. Техническое задание",
            "2. Обоснование ЗКО",
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    @contextmanager
    def calculation_nmc(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}calc_NMC/calc_zatrat.xlsx", "rb"),
                "caption": "Шаблон №1. Расчет НМЦ (затратный метод)",
            },
            {
                "file": open(f"{PARRENT_PATH}calc_NMC/calc_rinok.xlsx", "rb"),
                "caption": "Шаблон №2. Расчет НМЦ (метод сопоставимых рыночных цен)",
            },
            {
                "file": open(f"{PARRENT_PATH}calc_NMC/calc_tarif.xlsx", "rb"),
                "caption": "Шаблон №3. Расчет НМЦ (тарифный метод)",
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)
