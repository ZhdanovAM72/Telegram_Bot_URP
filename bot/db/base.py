from bot.db.create import CreateMethods
from bot.db.delete_utils import DeleteMethods
from bot.db.permissions import CheckPermissionsMethods
from bot.db.search import SearchMethods
from bot.db.update import UpdateMethods


class BaseBotBbMethods(
    CreateMethods, DeleteMethods, CheckPermissionsMethods,
    SearchMethods, UpdateMethods
):
    pass
