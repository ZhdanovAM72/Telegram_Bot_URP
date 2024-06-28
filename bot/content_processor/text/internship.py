from telebot import types
from bot.utils.documents import Documents
from bot import bot


class Internship:

    def internship(message: types.Message) -> types.Message:
        message_text = (
            'СТАЖИРОВКА \nПозволяет работнику погрузиться '
            'в другую деятельность и получить новый опыт в короткие'
            ' сроки. \nПеред началом стажировки совместно с '
            'руководителем необходимо сформировать план на время '
            'стажировки и согласовать его с наставником '
            'принимающей стороны.\n '
            '\nОбязательства принимающей стороны:\n'
            '- Подготовка рабочего места для стажера.\n'
            '- Выполнение плана работы на время стажировки.\n'
            '- Консультирование и сопровождение стажера. \n'
            '- Экспертная помощь наставника.'
        )
        bot.send_message(message.chat.id, message_text)
        parrent_path = 'prod_data/Стажировка/'
        documents = (
            f'{parrent_path}Стажировки_БРД.pdf',
            f'{parrent_path}Бланк_плана_стажировки_сотрудника.xlsx',
        )
        captions = (
            'Стажировки описание процесса',
            'Бланк плана стажировки сотрудника',
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)
