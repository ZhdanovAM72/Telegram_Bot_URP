from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
# from bot.constant import ES, ITS, NR, ST


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

    def education(message: types.Message) -> types.Message:
        buttons = [
            'Цикл планирования обучения',
            'Каталог программ',
            'Полезная литература',
            'Планирование обучения',
            '🔙 вернуться в раздел Цикл управления талантами',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ Обучение",
            reply_markup=markup,
        )

    def planning_education(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Обучение/ГПН_ЭС/plan/'
        documents = (
            {
                'file': open(f'{parrent_path}employee.pdf', 'rb'),
                'caption': 'Планирование обучения - Сотрудник',
            },
            {
                'file': open(f'{parrent_path}supervisor.pdf', 'rb'),
                'caption': 'Планирование обучения - Руководитель',
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)
