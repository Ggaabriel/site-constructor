from typing import Callable

from fastapi import status

from ..setup import client

"""
### POST /projects/by/user/{user_id}

user-init-data:

1. пользователь существует
2. пользователь не существует
3. неправильный формат

- (1) - 201 - проект действительно создался у пользователя, имя проекта совпадает
- (2) - 401
- (3) - 401
"""


# (1)
def test_create_project(create_user: Callable) -> None:
    """(1) - 201 - проект создался у пользователя"""
    _, user_init_data = create_user()
    name = client.get_random_project_name()

    response = client.create_project(
        project_name=name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_201_CREATED


# (2)
def test_try_create_project_for_unexistent_user() -> None:
    """(2) - 401 - пользователь не существует"""
    _, user_init_data = client.get_random_user()
    name = client.get_random_project_name()

    response = client.create_project(
        project_name=name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3)
def test_try_create_project_with_bad_token() -> None:
    """(3) - 401 - неправильный формат"""
    user_init_data = "bad-format"
    name = client.get_random_project_name()

    response = client.create_project(
        project_name=name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
