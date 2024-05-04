import datetime as dt

from telebot import types

from bot import bot
from bot.utils.check_permission import CheckUserPermission
from bot.utils.documents import Documents
from bot.utils.excel_export import ExcelExport
from bot.logger_setting.logger_bot import logger, log_user_command_updated


class BotInfoCommands:

    @classmethod
    def export_info(cls, message: types.Message) -> types.Message | None:
        """Экспортируем БД."""
        if not CheckUserPermission.check_admin(message):
            logger.warning(log_user_command_updated(message))
            return None

        bot.send_message(message.chat.id, 'Попытка экспорта данных.')
        ExcelExport.excel_export()
        date_info = dt.datetime.utcfromtimestamp(message.date)

        documents = (
            "result.xlsx",
            "bot_log.txt",
            "users_v2.sqlite",
        )
        captions = (
            f'Выгрузка БД на {date_info.date()}',
            f'Логи на {date_info.date()}',
            f'Файл БД {date_info.date()}',
        )
        logger.info(log_user_command_updated(message))
        return Documents.send_document_with_markup(message.chat.id, documents, captions)
