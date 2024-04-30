from bot.bot_command.start import StartBotCommand
from bot.bot_command.stop import StopBotCommand
from bot.bot_command.admin import AdminBotCommands
from bot.bot_command.moderator import ModeratorBotCommands
from bot.bot_command.register import RegisterUserCommand
from bot.bot_command.create_code import CreateCodeCommands
from bot.bot_command.bot_info import BotInfoCommands
from bot.bot_command.sending_messages import SendingMessagesBotCommands


class BaseBotCommands(
    StartBotCommand,
    StopBotCommand,
    AdminBotCommands,
    ModeratorBotCommands,
    RegisterUserCommand,
    CreateCodeCommands,
    BotInfoCommands,
    SendingMessagesBotCommands,
):
    pass
