from .projects import ApiProjects
from .users import ApiUsers


class ClientApi(ApiUsers, ApiProjects):
    pass
