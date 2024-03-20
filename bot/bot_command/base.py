from bot.bot_command.start import StartBotCommand
from bot.bot_command.stop import StopBotCommand
from bot.bot_command.admin import AdminBotCommands
from bot.bot_command.moderator import ModeratorBotCommands


class BaseBotCommands(
    StartBotCommand,
    StopBotCommand,
    AdminBotCommands,
    ModeratorBotCommands
):
    pass
