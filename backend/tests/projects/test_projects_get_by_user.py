from typing import Callable

from fastapi import status

from ..setup import client

"""
### GET /projects/by/user/{user_id}

user-init-data:

1. пользователь существует
2. пользователь не существует
3. неправильный формат

user_id:

1. пользователь существует и совпадает с id инициатора
2. пользователь существует и не совпадает с id инициатора
3. пользователь не существует

- (1, 1) - 200 - проекты пользователя действительно отображают список его проектов
- (1, 2) - 403
- (1, 3) - 404
- (2, 1) - 401
- (2, 2) - 401
- (2, 3) - 401
- (3, 1) - 401
- (3, 2) - 401
- (3, 3) - 401
"""


# (1, 1) - несколько проектов
def test_get_projects_many(create_user: Callable, create_project: Callable) -> None:
    """(1, 1) - 200 - полученные проекты совпадают с созданными"""
    user, user_init_data = create_user()

    amount = 10
    projects = []
    for _ in range(amount):
        project = create_project(user_init_data=user_init_data)
        projects.append(project)

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == amount

    for project, project_get in zip(
        sorted(projects, key=lambda project: project.id),
        sorted(response.json(), key=lambda project: project["id"]),
    ):
        assert project.owner_id == project_get["owner_id"]
        assert project.id == project_get["id"]
        assert project.name == project_get["name"]


# (1, 1) - нет проектов
def test_get_projects_empty(create_user: Callable) -> None:
    user, user_init_data = create_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


# (1, 2)
def test_try_get_another_projects(create_user: Callable) -> None:
    """(1, 2) - 403"""
    _, user_init_data = create_user()
    user, _ = create_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 3)
def test_try_get_another_projects_for_nonexistent_user(create_user: Callable) -> None:
    """(1, 3) - 404"""
    _, user_init_data = create_user()
    user, _ = client.get_random_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# (2, 1), (2, 2)
def test_try_get_projects_from_nonexistent_user(create_user: Callable) -> None:
    """(2, 1), (2, 2) - 401"""
    _, user_init_data = client.get_random_user()
    user, _ = create_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 3)
def test_try_get_projects_from_nonexistent_user_for_nonexistent_user() -> None:
    """(2, 3) - 401"""
    _, user_init_data = client.get_random_user()
    user, _ = client.get_random_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1), (3, 2)
def test_try_get_projects_with_bad_token(create_user: Callable) -> None:
    """(3, 1), (3, 2) - 401"""
    user_init_data = "bad-format"
    user, _ = create_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 3)
def test_try_get_projects_with_bad_token_for_nonexistent_user() -> None:
    """(3, 3) - 401"""
    user_init_data = "bad-format"
    user, _ = client.get_random_user()

    response = client.get_projects_by_user(
        user_id=user["id"],
        user_init_data=user_init_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
