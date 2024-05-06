from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class TalentManagementCycle:

    def talent_management_cycle(message: types.Message) -> types.Message:
        buttons = [
            'Обучение',
            'Регулярная оценка',
            'Диалоги об эффективности',
            'Комитеты по талантам',
            'Диалоги о развитии',
            '🔙 Главное меню',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ Цикл управления талантами",
            reply_markup=markup,
        )

    def regular_assessment(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Цикл_управления_талантами/Регулярная_оценка/'
        documents = (
            f'{parrent_path}instruction.pdf',
            f'{parrent_path}для_сотрудников.pdf',
            f'{parrent_path}reg_360.pdf',
        )
        captions = (
            'Инструкция по чтению отчета регулярной оценки',
            'Регулярная оценка для сотрудников',
            'Брошюра регулярной оценки 360',
        )
        buttons = [
            ["смотреть видео", "https://youtu.be/yxILbJcIFA8"]
        ]
        markup = Buttons.create_inline_keyboard(buttons)
        bot.send_message(
            message.chat.id,
            '⬇ Комплексная оценка 360 градусов',
            reply_markup=markup,
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    def contribution_evaluation_commission(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Цикл_управления_талантами/Регулярная_оценка'
        document = (f'{parrent_path}/Комиссия.pdf',)
        caption = ('Комиссия по оценке вклада для сотрудников',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def dialogues_about_efficiency(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Цикл_управления_талантами/Диалоги_об_эффективности/'
        documents = (
            f'{parrent_path}dialog.pdf',
            f'{parrent_path}ДоЭФ.PNG',
        )
        captions = (
            'Диалог об эффективности - Памятка для сотрудника',
            'Помятка для сотрудника',
        )
        buttons = [
            ["смотреть видео", "https://youtu.be/O2JyX9iL8Hs"]
        ]
        markup = Buttons.create_inline_keyboard(buttons)
        bot.send_message(
            message.chat.id,
            '⬇ Диалог об эффективности',
            reply_markup=markup,
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    def talent_committees(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Цикл_управления_талантами/comitet/'
        documents = (
            {
                'file': open(f'{parrent_path}nmd.pdf', 'rb'),
                'caption': 'Комитет по талантам - процедура проведения',
            },
            {
                'file': open(f'{parrent_path}PR_criteria.pdf', 'rb'),
                'caption': 'Критерии включения в кадровый резерв',
            },
            {
                'file': open(f'{parrent_path}rules.pdf', 'rb'),
                'caption': 'Правила нахождения в кадровом резерве',
            },
        )
        buttons = [
            ["смотреть видео", "https://youtu.be/O2JyX9iL8Hs"]
        ]
        markup = Buttons.create_inline_keyboard(buttons)
        bot.send_message(
            message.chat.id,
            '⬇ Комитеты по талантам',
            reply_markup=markup,
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)

    def development_dialogues(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Цикл_управления_талантами/Диалоги_о_развитии/'
        documents = (
            {
                'file': open(f'{parrent_path}Методология.pdf', 'rb'),
                'caption': 'Диалог о развитии - Методология',
            },
            {
                'file': open(f'{parrent_path}difference.pdf', 'rb'),
                'caption': 'Разница между диалогом о развитии и диалогом об эффективности',
            },
        )
        buttons = [
            ["смотреть видео", "https://youtu.be/HZB4eES30XI"]
        ]
        markup = Buttons.create_inline_keyboard(buttons)
        bot.send_message(
            message.chat.id,
            '⬇ Диалоги о развитии',
            reply_markup=markup,
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)
