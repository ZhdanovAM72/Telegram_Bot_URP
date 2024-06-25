import os
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
        accounts_count, users_count = ExcelExport.excel_export_new()
        date_info = dt.datetime.utcfromtimestamp(message.date)

        excel_document = (
            "result.xlsx",
        )
        excel_caption = (
            f'Выгрузка дынных из БД на {date_info.date()}, \n'
            f'Учетных записей всего: {accounts_count if accounts_count else 0} шт.\n'
            f'Зарегистрировано: {users_count if users_count else 0} сотрудника(ов).',
        )
        logger.info(log_user_command_updated(message))
        return Documents.send_document_with_markup(message.chat.id, excel_document, excel_caption)

    @classmethod
    def export_logs(cls, message: types.Message) -> types.Message | None:
        """Экспортируем логи."""
        if not CheckUserPermission.check_admin(message):
            logger.warning(log_user_command_updated(message))
            return None

        bot.send_message(message.chat.id, 'Попытка экспорта данных.')
        date_info = dt.datetime.utcfromtimestamp(message.date)

        log_documents = [file for file in os.listdir('.') if file.startswith("bot_log")]
        log_caption = [f'Логи на {date_info.date()}' for _ in log_documents]
        logger.info(log_user_command_updated(message))
        return Documents.send_document_with_markup(message.chat.id, log_documents, log_caption)
