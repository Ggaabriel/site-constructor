from typing import Callable

from fastapi import status

from ..setup import client

"""
### GET /users/{user_id}

user-init-data:

1. пользователь существует
2. пользователь не существует
3. неправильный формат

user_id:

1. пользователь существует и совпадает с id инициатора
2. пользователь существует и не совпадает с id инициатора
3. пользователь не существует

- (1, 1) - 200, возвращаемый id совпадает с запрашиваемым
- (1, 2) - 403
- (1, 3) - 404 (?)
- (2, 1) - 401
- (2, 2) - 401
- (2, 3) - 401
- (3, 1) - 401
- (3, 2) - 401
- (3, 3) - 401
"""


# (1, 1)
def test_get_user(create_user: Callable) -> None:
    """(1, 1) - 200, возвращаемый id совпадает с запрашиваемым"""
    user, user_init_data = create_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user


# (1, 2)
def test_try_get_another_user(create_user: Callable) -> None:
    """(1, 2) - 403 - пользователь не совпадает с id инициатора"""
    _, user_init_data = create_user()
    user, _ = create_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# (1, 3)
def test_try_get_another_nonexistent_user(create_user: Callable) -> None:
    """(1, 3) - 404 - инициатор существует, пользователь не существует"""
    _, user_init_data = create_user()
    user, _ = client.get_random_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# (2, 1), (2, 2)
def test_try_get_another_user_from_nonexistent_user(create_user: Callable) -> None:
    """(2, 1) - 401 - инициатор не существует, пользователь существует"""
    _, user_init_data = client.get_random_user()
    user, _ = create_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (2, 3)
def test_try_get_another_nonexistent_user_from_nonexistent_user(
    create_user: Callable,
) -> None:
    """(2, 3) - 401 - инициатор и пользователь не существуют"""
    _, user_init_data = client.get_random_user()
    user, _ = client.get_random_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 1), (3, 2)
def test_try_get_user_with_bad_token(create_user: Callable) -> None:
    """(3, 1) - 404 - неправильный формат user-init-data, пользователь существует"""
    user_init_data = "bad-format"
    user, _ = create_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# (3, 3)
def test_try_get_nonexistent_user_with_bad_token(create_user: Callable) -> None:
    """(3, 1) - 404 - неправильный формат user-init-data , пользователь не существует"""
    user_init_data = "bad-format"
    user, _ = client.get_random_user()

    response = client.get_user(
        user_init_data=user_init_data,
        user_id=user["id"],
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
