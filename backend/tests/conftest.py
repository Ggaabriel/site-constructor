from dataclasses import dataclass
from typing import Callable

import pytest
from fastapi import status

from .setup import client


@dataclass
class Project:
    """
    name: str
    id: str
    core_node_id: str
    owner_id: str
    """

    name: str
    id: str
    core_node_id: str
    owner_id: str


@pytest.fixture
def create_user() -> Callable[[], tuple[dict[str, str], str]]:
    def _create_user() -> tuple[dict[str, str], str]:
        user, user_init_data = client.get_random_user()

        response = client.create_user(
            user_id=user["id"],
        )
        assert response.status_code == status.HTTP_201_CREATED

        return user, user_init_data

    return _create_user


@pytest.fixture
def create_project() -> Callable[[str], Project]:
    def _create_project(user_init_data: str) -> Project:
        name = client.get_random_project_name()

        response = client.create_project(
            project_name=name,
            user_init_data=user_init_data,
        )

        project = Project(**response.json())

        assert response.status_code == status.HTTP_201_CREATED

        return project

    return _create_project
