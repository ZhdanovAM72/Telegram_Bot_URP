from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, ST


class Adaptation:

    def adaptation(message: types.Message) -> types.Message:
        buttons = (
            'Корпоративная безопасность',
            'Производственная безопасность',
            'Хоз. и транспорт. обеспечение',
            'Трудовой распорядок',
            'Внешний вид. Спецодежда и СИЗ',
            'Мотивация персонала',
            'Буклеты для сотрудников',
            'Книги для сотрудников',
            '🔙 Главное меню',
        )
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="Адаптация",
            reply_markup=markup,
        )

    def corporate_security(message: types.Message) -> types.Message:
        buttons = (
            (
                "открыть канал",
                'https://lenta.gazprom-neft.ru/channel/kiberbezopasnost_novosti_i_pravila_bezopasnoy_raboty/'
            ),
        )
        markup = Buttons.create_inline_keyboard(buttons=buttons, row_width=1)
        bot.send_message(
            message.chat.id,
            text='Мобильная лента Кибербезопасность. Новости и правила безопасной работы.',
            reply_markup=markup,
        )
        parrent_path = 'prod_data/Адаптация/корпоративная_безопасность/'
        document = (
            f'{parrent_path}ES.pdf',
            f'{parrent_path}памятка.pdf',
            f'{parrent_path}ITS.pdf',
            f'{parrent_path}ST.pdf',
        )
        caption = (
            f'Корпоративная безопасность {ES}',
            'Памятка по информационной безопасности',
            f'Корпоративная безопасность {ITS}',
            f'Корпоративная безопасность {NR} и {ST}',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def industrial_safety(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Адаптация/производственная_безопасность/'
        document = (
            f'{parrent_path}ES_pb.pdf',
            f'{parrent_path}ITS_pb.pdf',
            f'{parrent_path}ST_NR_pb.pdf',
        )
        caption = (
            f'Производственная безопасность {ES}',
            f'Производственная безопасность {ITS}',
            f'Производственная безопасность {NR} и {ST}',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def economic_and_transport_support(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Адаптация/hoz_trans/'
        document = (
            f'{parrent_path}ES.pdf',
            f'{parrent_path}ITS.pdf',
            f'{parrent_path}NR.pdf',
            f'{parrent_path}ST.pdf',
        )
        caption = (
            f'Хозяйственное и транспортное обеспечение {ES}',
            f'Хозяйственное и транспортное обеспечение {ITS}',
            f'Хозяйственное и транспортное обеспечение {NR}',
            f'Хозяйственное и транспортное обеспечение {ST}',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def work_schedule(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Адаптация/trudovoi_raspor/'
        document = (
            f'{parrent_path}es_trud.pdf',
            f'{parrent_path}its_trud.pdf',
            f'{parrent_path}nr_trud.pdf',
            f'{parrent_path}st_trud.pdf',
        )
        caption = (
            f'Трудовой распорядок в {ES}',
            f'Трудовой распорядок в {ITS}',
            f'Трудовой распорядок в {NR}',
            f'Трудовой распорядок в {ST}',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def workwear(message: types.Message) -> types.Message:
        document = ('prod_data/Адаптация/vnesh_vid/vneshsiz.pdf',)
        caption = ('Внешний вид. Спецодежда и СИЗ',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def staff_motivation(message: types.Message) -> types.Message:
        buttons = (
            'Мотивация ЭС',
            'Мотивация НР',
            'Мотивация ИТС',
            'Мотивация СТ',
            '🔙 вернуться в раздел Адаптация',
        )
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            text="⬇ Мотивация персонала",
            reply_markup=markup,
        )

    def motivation_es(message: types.Message) -> types.Message:
        document = ('prod_data/Адаптация/мотивация_персонала/ES_motivate.pdf',)
        caption = (f'Мотивация сотрудников {ES}',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def motivation_nr(message: types.Message) -> types.Message:
        document = ('prod_data/Адаптация/мотивация_персонала/NR_motivate.pdf',)
        caption = (f'Мотивация сотрудников {NR}',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def motivation_its(message: types.Message) -> types.Message:
        document = ('prod_data/Адаптация/мотивация_персонала/ITS_motivate.pdf',)
        caption = (f'Мотивация сотрудников {ITS}',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def motivation_st(message: types.Message) -> types.Message:
        document = ('prod_data/Адаптация/мотивация_персонала/ST_motivate.pdf',)
        caption = (f'Мотивация сотрудников {ST}',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def booklets_for_employees(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Адаптация/буклеты_для_сотрудников/'
        document = (
            f'{parrent_path}ES_2024.pdf',
            f'{parrent_path}NR_2023.pdf',
            f'{parrent_path}ST_2023.pdf',
        )
        caption = (
            f'Буклет сотрудника {ES}.',
            f'Буклет сотрудника {NR}.',
            f'Буклет сотрудника {ST}.',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def books_for_employees(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Адаптация/книги_для_новых_сотрудников/'
        document = (
            f'{parrent_path}ES_book.pdf',
            f'{parrent_path}NR_book.pdf',
            f'{parrent_path}ITS_book.pdf',
            f'{parrent_path}ST_book.pdf',
        )
        caption = (
            f'Книга для нового сотрудника {ES}',
            f'Книга для нового сотрудника {NR}',
            f'Книга для нового сотрудника {ITS}',
            f'Книга для нового сотрудника {ST}',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)
