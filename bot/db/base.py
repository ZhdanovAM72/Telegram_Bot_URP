from bot.db.create_new import CreateMethods

from bot.db.delete_utils import DeleteMethods
from bot.db.permissions import CheckPermissionsMethods
from bot.db.search import SearchMethods
from bot.db.update import UpdateMethods


class BaseBotBbMethods(
    DeleteMethods, CheckPermissionsMethods,
    SearchMethods, UpdateMethods, CreateMethods
):
    pass
