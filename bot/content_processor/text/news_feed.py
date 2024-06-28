from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class NewsFeed:

    def news_feed(message: types.Message) -> types.Message:
        buttons = [
            'Корпоративный портал',
            'Мобильная лента',
            'Телеграм-каналы',
            '🔙 вернуться в раздел О компании',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            text="⬇ Новостная лента",
            reply_markup=markup,
        )

    def corporate_portal(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/о_компании/новостная_лента/corp_portal/'
        document = [f'{parrent_path}guide.pdf', f'{parrent_path}enter.pdf']
        caption = [
            'Как через Интернет войти на Портал знаний',
            'Как войти в личный кабинет на портале знаний',
        ]
        buttons = [
            ["Открыть портал знаний", "https://edu.gazprom-neft.ru"],
        ]
        markup = Buttons.create_inline_keyboard(buttons=buttons)
        bot.send_message(
            message.chat.id,
            'Корпоративные ресурсы',
            reply_markup=markup
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def mobile_feed(message: types.Message) -> types.Message:
        buttons = [
            ['КАНАЛ «ГАЗПРОМ НЕФТИ»', "HTTPS://LENTA.GAZPROM-NEFT.RU/"],
            ['КАНАЛ «НЕФТЕСЕРВИСЫ»', "https://lenta.gazprom-neft.ru/channel/nefteservisy/"],
        ]
        markup = Buttons.create_inline_keyboard(buttons=buttons, row_width=1)
        bot.send_message(
            message.chat.id,
            'Мобильная лента:\n'
            '\n'
            '1. КАНАЛ «ГАЗПРОМ НЕФТИ»\n Главные новости компании'
            ' емко и без лишних деталей, '
            'конкурсы, тесты, прямые трансляции с мероприятий,'
            ' каналы коллег о работе, '
            'корпоративной культуре, финансах, спорте и жизни.\n'
            '\n'
            '2. КАНАЛ «НЕФТЕСЕРВИСЫ»\n Канал для блока '
            'нефтесервисов: '
            'Нефтесервисных решений, Энергосистем, ННГГФ, Сервисных'
            ' технологий со всеми видами активностей:'
            ' опросы, конкурсы, публикация новостей, '
            'комментарии участников.',
            reply_markup=markup,
        )

    def telegram_channels(message: types.Message) -> types.Message:
        buttons = [
            ['КУЛЬТУРА И СПОРТ БРД', "HTTPS://T.ME/SPORTCULTUREBRDHR"],
            ['Новости нефтесервисов', "https://t.me/+LmDKSVvewR0yMzEy"],
            ['Совет молодых специалистов', "https://t.me/+b-xEPVRlQr4zMmI6"],
            ['НТК', "https://t.me/+TJe7-1a28tSJS-7Q"],
        ]
        markup = Buttons.create_inline_keyboard(buttons=buttons, row_width=1)
        bot.send_message(
            message.chat.id,
            'Телеграм-каналы:\n\n'
            '1. «Культура и спорт БРД» \nОперативная, '
            'актуальная и эксклюзивная информация '
            'про культуру, спорт и не только!\n\n'
            '2. «Новости нефтесервисов» \nНовости из '
            'жизни нефтесервисов.\n\n'
            '3. «Совет молодых специалистов» '
            'Актуальная информация о деятельности '
            'Совета молодых специалистов.\n\n'
            '4. «Научно-техническая конференция» \n'
            'Актуальная информация о молодежной '
            'научно-технической конференции.\n',
            reply_markup=markup,
        )
