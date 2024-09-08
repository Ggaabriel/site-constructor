from typing import Callable

from fastapi import status

from ..setup import client

"""
### PATCH /projects/{project_id}

user-init-data:

1. пользователь существует
2. пользователь не существует
3. неправильный формат

project_id:

1. существует и принадлежит инициатору
2. существует и не принадлежит инициатору
3. не существует

- (1, 1) - 200 - имя проекта действительно обновилось
- (1, 2) - 403
- (1, 3) - 404
- (2, 1) - 401
- (2, 2) - 401
- (2, 3) - 401
- (3, 1) - 401
- (3, 2) - 401
- (3, 3) - 401
"""


# (1, 1)
def test_update_project(create_user: Callable, create_project: Callable) -> None:
    """(1, 1) - 200 - имя проекта действительно обновилось"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    new_name = "new_name"

    response = client.update_project(
        project_id=project.id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.get_project_by_id(
        project_id=project.id,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == new_name


# (1, 2)
def test_try_update_another_project(
    create_user: Callable, create_project: Callable
) -> None:
    """(1, 2) - 403"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    _, user_init_data = create_user()

    new_name = "new_name"

    response = client.update_project(
        project_id=project.id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 3)
def test_try_update_nonexistent_project(create_user: Callable) -> None:
    """(1, 3) - 404"""
    _, user_init_data = create_user()
    project_id = "0"

    new_name = "new_name"

    response = client.update_project(
        project_id=project_id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# (2, 1), (2, 2)
def test_try_update_project_from_nonexistent_user(
    create_user: Callable, create_project: Callable
) -> None:
    """(2, 1), (2, 2) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)
    _, user_init_data = client.get_random_user()

    new_name = "new_name"

    response = client.update_project(
        project_id=project.id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 3)
def test_try_update_nonexistent_project_from_nonexistent_user(
    create_user: Callable,
) -> None:
    """(2, 3) - 401"""
    _, user_init_data = client.get_random_user()
    project_id = "0"

    new_name = "new_name"

    response = client.update_project(
        project_id=project_id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1), (3, 2)
def test_try_update_project_with_bad_token(
    create_user: Callable, create_project: Callable
) -> None:
    """(3, 1), (3, 2) - 401"""
    _, user_init_data = create_user()
    project = create_project(user_init_data=user_init_data)

    user_init_data = "bad-format"

    new_name = "new_name"

    response = client.update_project(
        project_id=project.id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 3)
def test_try_update_nonexistent_project_with_bad_token(
    create_user: Callable, create_project: Callable
) -> None:
    """(3, 3) - 401"""
    user_init_data = "bad-format"
    project_id = "0"

    new_name = "new_name"

    response = client.update_project(
        project_id=project_id,
        name=new_name,
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
