from app.registry import IRegistry

from ..exceptions import (
    NotAllowedError,
    UserExistError,
    UserNotFoundError,
    WrongInitiatorError,
)
from ..FileService import IFileService
from .IUserService import IUserService
from .schemas.UserCreateSchema import UserCreateSchema
from .schemas.UserId import UserId
from .schemas.UserSchema import UserSchema


class UserService(IUserService):
    """
    A service class for managing user-related operations.
    """

    __registry: IRegistry
    __file_service: IFileService

    def __init__(self, registry: IRegistry) -> None:
        """
        Initialize the UserService with a registry.

        Parameters:
            registry (IRegistry): The registry to use for user operations.
        """
        self.__registry = registry

    async def inject_dependencies(self, file_service: IFileService) -> None:
        self.__file_service = file_service

    async def user_exist_validation(self, user_id: UserId) -> None:
        """
        Checks the existence of the user by his ID.

        Parameters:
            user_id (str): The ID of the user to check.

        Raises:
            WrongInitiatorError: if the user does not exist.
        """
        if not await self.exist(user_id):
            raise WrongInitiatorError()

    async def try_get_by_id(self, initiator_id: UserId, user_id: UserId) -> UserSchema:
        """
        Attempt to retrieve user information by user ID.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserSchema: The user information.

        Raises:
            WrongInitiatorError: if the user does not exist.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            UserNotFoundError: If the user with the specified ID is not found.
        """
        await self.user_exist_validation(initiator_id)
        user = await self.__get_by_id(user_id)
        if initiator_id != user_id:
            raise NotAllowedError()
        return user

    async def create(self, new_user: UserCreateSchema) -> None:
        """
        Create a new user.

        Parameters:
            new_user (UserCreateSchema): The schema representing the new user
            to create.

        Raises:
            UserExistError: If a user with the same ID already exists.
        """
        if await self.exist(new_user.id):
            raise UserExistError()
        user = UserSchema(**new_user.model_dump())
        self.__registry.create(user.id, user.model_dump(exclude={"id"}))
        await self.__file_service.create_folder("", user.id)

    async def exist(self, user_id: UserId) -> bool:
        """
        Check if a user exists based on the provided ID.

        Parameters:
            user_id (str): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        result = self.__registry.get(user_id)
        return result is not None

    async def __get_by_id(self, user_id: UserId) -> UserSchema:
        """
        Get user information by ID.

        Parameters:
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserSchema: The user information.

        Raises:
            UserNotFoundError: If the user with the specified ID is not found.
        """
        result = self.__registry.get(user_id)
        if result is None:
            raise UserNotFoundError()
        return UserSchema(**result)
