from bot.bot_command.start import StartBotCommand
from bot.bot_command.stop import StopBotCommand


class BaseBotCommands(StartBotCommand, StopBotCommand):
    pass
