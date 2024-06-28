from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, ST


class AboutCompany:

    def about_company(message: types.Message) -> types.Message:
        buttons = [
            "Выбрать ДО",
            "Корпоративные ценности",
            "Сервисы для сотрудников",
            "Новостная лента",
            "Корпоративная этика",
            "🔙 Главное меню",
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ О компании",
            reply_markup=markup,
        )

    def choose_do(message: types.Message) -> types.Message:
        buttons = [
            'Нефтесервисные решения',
            'Газпромнефть Энергосистемы',
            'Инженерно-технологический сервис',
            'Газпромнефть Сервисные технологии',
            '🔙 вернуться в раздел О компании',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Выбрать ДО",
            reply_markup=markup
        )

    def do_st(message: types.Message) -> types.Message:
        buttons = [
            'Структура СТ',
            'История СТ',
            '🔙 вернуться в раздел Выбрать ДО',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Газпромнефть Сервисные технологии",
            reply_markup=markup
        )

    def history_st(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/СТ/история/about_us.pdf']
        caption = [f'История {ST}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def structure_st(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/СТ/структура/structure.pdf']
        caption = [f'Структура {ST}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def do_nr(message: types.Message) -> types.Message:
        buttons = [
            'История НР',
            '🔙 вернуться в раздел Выбрать ДО',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Нефтесервисные решения",
            reply_markup=markup
        )

    def history_nr(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/НР/История/about_us.pdf']
        caption = [f'История {NR}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def structure_nr(message: types.Message) -> types.Message:
        document = ('prod_data/о_компании/выбрать_ДО/НР/structure.pdf',)
        caption = (f'Структура {NR}',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def do_its(message: types.Message) -> types.Message:
        buttons = [
            'Структура ИТС',
            'НМД ИТС',
            'Контакты ИТС',
            'История ИТС',
            '🔙 вернуться в раздел Выбрать ДО',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Инженерно-технологический сервис",
            reply_markup=markup
        )

    def contacts_its(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ННГГФ/Контакты/info.pdf']
        caption = [f'Контакты {ITS}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def history_its(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ННГГФ/История/about_us.pdf']
        caption = [f'История {ITS}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def structure_its(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ННГГФ/Структура/structure.pdf']
        caption = [f'Структура {ITS}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def nmd_its(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/о_компании/выбрать_ДО/ННГГФ/НМД/'
        document = [
            f'{parrent_path}8.pdf',
            f'{parrent_path}ptvr.pdf',
            f'{parrent_path}vahta.pdf',
        ]
        caption = [
            f'Пропускной и внутреобъектовый режимы {ITS}',
            f'Правила внутреннего трудового распорядка {ITS}',
            f'Положение о вахтовом методе работы {ITS}',
        ]
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def do_es(message: types.Message) -> types.Message:
        buttons = [
            'История Энергосистем',
            'Структура Энергосистем',
            'Контакты Энергосистем',
            '🔙 вернуться в раздел Выбрать ДО',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Газпромнефть Энергосистемы",
            reply_markup=markup
        )

    def history_es(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ГПН_ЭС/история/about_us.pdf']
        caption = [f'История {ES}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def structure_es(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ГПН_ЭС/Структура/'
                    'организационная_структура_ЭС.pdf']
        caption = [f'Структура компании {ES}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def contacts_es(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/выбрать_ДО/ГПН_ЭС/контакты/contacs.pdf']
        caption = [f'Контакты компании {ES}']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def corporate_values(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/корпоративные_ценности/gpn_guide.pdf']
        caption = ['Корпоративные ценности']
        Documents.send_document_with_markup(message.chat.id, document, caption)
