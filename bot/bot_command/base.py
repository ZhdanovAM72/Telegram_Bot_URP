from bot.bot_command.start import StartBotCommand
from bot.bot_command.stop import StopBotCommand
from bot.bot_command.admin import AdminBotCommands


class BaseBotCommands(StartBotCommand, StopBotCommand, AdminBotCommands):
    pass
