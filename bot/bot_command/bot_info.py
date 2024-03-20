import datetime as dt

from telebot import types

from bot import bot
from bot.db import BaseBotSQLMethods
from bot.utils.check_permission import CheckUserPermission
from bot.utils.code_generator import CodeGenerator
from bot.utils.excel_export import ExcelExport
from bot.logger_setting.logger_bot import log_user_command


class BotInfoCommands:

    @classmethod
    def export_info(cls, message: types.Message) -> None:
        """Экспортируем БД."""
        if not CheckUserPermission.check_admin(message):
            return log_user_command(message)

        bot.send_message(message.chat.id, 'Попытка экспорта данных.')
        ExcelExport.excel_export()
        export_document_1 = 'result.xlsx'
        export_document_2 = 'bot_log.txt'
        export_document_3 = 'users_v2.sqlite'
        date_info = dt.datetime.utcfromtimestamp(message.date)
        with open(export_document_1, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=f'Выгрузка БД на {date_info.date()}',
                parse_mode="html"
            )
        with open(export_document_2, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=f'Логи на {date_info.date()}',
                parse_mode="html"
            )
        with open(export_document_3, 'rb') as file:
            bot.send_document(
                message.chat.id,
                file,
                caption=f'Файл БД {date_info.date()}',
                parse_mode="html"
            )
        return log_user_command(message)
