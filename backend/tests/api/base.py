from typing import Optional
from uuid import uuid4

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient


class ApiBase:
    """
    API wrapper for testing endpoints
    """

    API_V1 = "/api/v1"

    USERS = API_V1 + "/users"
    PROJECTS = API_V1 + "/projects"

    USER = USERS + "/{user_id}"
    PROJECT = PROJECTS + "/{project_id}"
    PROJECT_BY_USER = PROJECTS + "/by/user/{user_id}"

    def __init__(self, app: FastAPI):
        self.client = TestClient(app)

    def get_random_user(self) -> tuple[dict[str, str], str]:
        """
        Generates a random user object and corresponding user-specific data string.

        Returns:
            tuple[dict, str]: A tuple containing two elements:
            - A dict representing a random user with an ID generated using UUID4.
            - A string in the format `user={"id": "..."}` containing the user ID.
        """

        _id = str(uuid4())
        return {"id": _id}, f'user={{"id": "{_id}"}}'

    def get_random_project_name(self) -> str:
        """
        Generates a random project name with a prefix and truncated UUID4.

        Returns:
            str: A string representing a random project name, \
                e.g., "project-e427ab1234".
        """
        return f"project-{str(uuid4())[:10]}"

    def post(
        self,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a POST HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            json (dict, optional): JSON data to include in the request body. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.post(
            url=url,
            json=json,
            headers=headers,
        )

    def get(
        self,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a GET HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            params (dict, optional): Query parameters to include in the request. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.get(
            url=url,
            params=params,
            headers=headers,
        )

    def delete(
        self,
        url: str,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a DELETE HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """
        headers = headers or dict()

        return self.client.delete(
            url=url,
            headers=headers,
        )

    def patch(
        self,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Sends a PATCH HTTP request to the specified URL.

        Args:
            url (str): The target URL for the request.
            json (dict, optional): JSON data to include in the request body. \
                Defaults to dict().
            headers (dict, optional): Additional headers to include in the request. \
                Defaults to dict().

        Returns:
            httpx.Response: The response object from the server.
        """

        return self.client.patch(
            url=url,
            json=json,
            headers=headers,
        )
