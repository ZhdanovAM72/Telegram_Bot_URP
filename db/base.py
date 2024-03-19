from .create import CreateMethods
from .delete_utils import DeleteMethods
from .permissions import CheckPermissionsMethods
from .search import SearchMethods
from .update import UpdateMethods


class BaseBotBbMethods(
    CreateMethods, DeleteMethods, CheckPermissionsMethods,
    SearchMethods, UpdateMethods
):
    pass
