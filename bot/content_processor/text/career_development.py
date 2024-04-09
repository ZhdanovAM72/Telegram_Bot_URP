from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class CareerDevelopment:

    def career_development(message: types.Message) -> types.Message:
        buttons = [
            'Мой трек',
            'Мой профиль',
            'Индивидуальный план развития',
            'Карьерное консультирование',
            '🔙 Главное меню',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ Карьерное развитие",
            reply_markup=markup,
        )

    def my_track(message: types.Message) -> types.Message:
        document = ['prod_data/карьерное_развитие/my_track/my.pdf']
        caption = ['Мой трек и карьерные опции']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def my_profile(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/карьерное_развитие/profile_on_portal/'
        document = [
            f'{parrent_path}info.pdf',
            f'{parrent_path}profile.pdf',
        ]
        caption = [
            'Памятка по заполнению профиля',
            'Профиль сотрудника',
        ]
        bot.send_message(
            message.chat.id,
            'Профиль на карьерном портале -это Ваша визитная карточка, '
            'в которой отображаются ваши уникальные навыки и квалификация,'
            ' она подчеркивает преимущества, которые вы можете '
            'предложить работодателю.\n'
            '\nЗдесь собирается вся информация о Вас как о специалисте:\n'
            '- информация об образовании,\n'
            '- профессиональной квалификации,\n'
            '- соответствующем опыте работы,\n'
            '- навыках и заметных достижениях\n'
            '\nРегулярно обновляйте профиль, чтобы руководители и HR '
            'смогли видеть самую актуальную информацию о Вас.',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def individual_development_plan(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/карьерное_развитие/individual_plan/'
        document = [
            f'{parrent_path}instruction.pdf',
            f'{parrent_path}IPR.pdf',
            f'{parrent_path}menu.pdf',
            f'{parrent_path}plan.pdf',
            f'{parrent_path}done.pdf',
        ]
        caption = [
            'Актуализация ИПР - Инструкция для сотрудников',
            'Формирование плана развития - Памятка для сотрудников 2023',
            'Меню развивающих действий',
            'Индивидуальный план развития - памятка для сотрудника',
            'Факт выполнения целей в ИПР',
        ]
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def career_counseling(message: types.Message) -> types.Message:
        document = ['prod_data/карьерное_развитие/carier_couch/file.png']
        caption = ['Карьерное консультирование']
        bot.send_message(
            message.chat.id,
            'Предмет карьерного консультирования — профессиональное и'
            'карьерное развитие сотрудника на протяжении '
            'всей его трудовой деятельности.\n'
            '\nЭто совместная деятельность карьерного консультанта '
            'и сотрудника по определению ценностей и профессиональных '
            'интересов, анализу ближайших и долгосрочных целей, '
            'ресурсов и возможностей сотрудника для достижения позитивных '
            'изменений в профессиональной деятельности.\n'
            '\nВы можете записаться на карьерную консультацию на'
            ' Карьерном портале при условии, что Ваш профиль '
            'заполнен не менее чем на 80%.',
        )
        Documents.send_document_with_markup(message.chat.id, document, caption)
