from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class DmsAndRvl:

    @staticmethod
    def dms_and_rvl(message: types.Message) -> types.Message:
        buttons = [
            'ДМС',
            'РВЛ',
            '🔙 Главное меню',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="ДМС и РВЛ",
            reply_markup=markup,
        )
        document = ['prod_data/ДМС/ГПН_ЭС/curators.pdf']
        caption = ['Кураторы программы в ДО и подразделениях']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    @contextmanager
    def dms(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/ДМС/ГПН_ЭС/ДМС/'
        documents = (
            {
                'file': open(f'{parrent_path}памятка_ДМС_2023.pdf', 'rb'),
                'caption': 'Памятка по лечению',
            },
            {
                'file': open(f'{parrent_path}med_list.xlsx', 'rb'),
                'caption': 'Перечень ЛПУ 2024 г.',
            },
            {
                'file': open(f'{parrent_path}dms.pdf', 'rb'),
                'caption': 'Возможности ДМС в НСА',
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    def rvl(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/ДМС/ГПН_ЭС/РВЛ/'
        document = [
            f'{parrent_path}памятка_санатории.pdf',
            f'{parrent_path}sanatoriums_list.xls',
        ]
        caption = [
            'Памятка по санаториям',
            'Перечень рекомендованных санаториев на 2024 г.',
        ]
        Documents.send_document_with_markup(message.chat.id, document, caption)
