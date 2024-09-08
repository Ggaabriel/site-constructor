import httpx

from .base import ApiBase


class ApiUsers(ApiBase):
    """
    Class representing an API client for interacting with the `/users` endpoints group.

    Inherits from `ApiBase` to provide common API interaction functionalities.
    """

    def create_user(
        self,
        user_id: str,
    ) -> httpx.Response:
        """
        Creates a new user on the `/users` endpoint.

        Args:
            user_id (str): The unique identifier for the new user.

        Returns:
            httpx.Response: The response object.
        """

        url = self.USERS
        json = {"id": user_id}

        return self.post(url=url, json=json)

    def get_user(
        self,
        user_init_data: str,
        user_id: str,
    ) -> httpx.Response:
        """
        Retrieves an existing user from the `/users` endpoint.

        Args:
            user_id (str): The unique identifier of the user to retrieve.
            user_init_data (str): User-specific initialization data required by the API.

        Returns:
            httpx.Response: The response object from the API containing user \
                information.
        """

        url = self.USER.format(user_id=user_id)
        headers = {
            "user-init-data": user_init_data,
        }

        return self.get(url=url, headers=headers)
