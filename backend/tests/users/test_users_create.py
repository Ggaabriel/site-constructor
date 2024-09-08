import pytest
from fastapi import status

from ..setup import client

"""
### POST /users

id:

1. Пользователя с таким id не существует
2. Пользователь с таким id уже существует

- (1) - 201 - пользователь действительно создался
- (2) - 409
"""


@pytest.fixture()
def create_user() -> tuple[dict[str, str], str]:
    user, user_init_data = client.get_random_user()

    response = client.create_user(
        user_id=user["id"],
    )
    assert response.status_code == status.HTTP_201_CREATED

    return user, user_init_data


# (1)
def test_create_user(create_user: tuple[dict[str, str], str]) -> None:
    """(1) - 201 - пользователь действительно создался"""
    user, user_init_data = create_user

    response = client.get_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user


# (2)
def test_try_create_existing_user(create_user: tuple[dict[str, str], str]) -> None:
    """(2) - 409 - пользователь с таким id уже существует"""
    user, _ = create_user

    response = client.create_user(
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_409_CONFLICT
