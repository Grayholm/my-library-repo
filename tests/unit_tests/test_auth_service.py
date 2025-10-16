from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.exceptions import NicknameIsEmptyException, LoginErrorException
from src.models.users import RoleEnum
from src.schemas.users import UserRequestAddRegister, UserLogin, UserWithHashedPassword, User
from src.services.auth import AuthService

@pytest.mark.asyncio
@pytest.mark.parametrize("data, expected_exception", [
    (
        UserRequestAddRegister(
            first_name='John',
            last_name='Doe',
            nickname='alexmercer',
            birth_day=date(2005, 12, 2),
            email='johndoe2005@gmail.com',
            password='gdxhgffdokw22jin',
        ),
        None  # Ожидаемое исключение - None (успех)
    ),
    (
        UserRequestAddRegister(
            nickname='alexmercer',
            email='johndoe2005@gmail.com',
            password='gdxhgffdokw22jin',
        ),
        None  # Ожидаемое исключение - None (успех)
    ),
    # Случай с пустым nickname
    (
        UserRequestAddRegister(
            first_name='John',
            last_name='Doe',
            nickname='',  # Пустой nickname
            birth_day=date(1990, 1, 1),
            email='test@example.com',
            password='password123',
        ),
        NicknameIsEmptyException
    ),
    # Случай с возрастом младше 18
    (
        UserRequestAddRegister(
            first_name='John',
            last_name='Doe',
            nickname='younguser',
            birth_day=date.today() - timedelta(days=365 * 17),  # 17 лет
            email='young@example.com',
            password='password123',
        ),
        HTTPException
    ),
])
async def test_register_user(data, expected_exception):
    mock_db = AsyncMock()
    mock_db.users.add = AsyncMock()
    mock_db.commit = AsyncMock()
    service = AuthService(mock_db)

    if expected_exception:
        with pytest.raises(expected_exception):
            await service.register_user(data)
    else:
        response = await service.register_user(data)
        assert response is not None
        assert 'message' in response
        assert response["message"] == "Вы успешно зарегистрировались!"
        mock_db.users.add.assert_called_once()
        mock_db.commit.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("data, expected_exception, password_correct", [
    (
        UserLogin(
            email='johndoe2005@gmail.com',
            password='password123',
        ),
        None,
        True
    ),
    (
        UserLogin(
            email='johndoe2005@gmail.com',
            password='password123',
        ),
        LoginErrorException,
        False
    )
])
async def test_login_and_get_access_token(data, expected_exception, password_correct):
    mock_db = AsyncMock()
    mock_user = UserWithHashedPassword(
        id=1,
        first_name='John',
        last_name='Doe',
        birth_day=date(2005, 12, 2),
        nickname='alexmercer',
        email=data.email,
        hashed_password='gdxhgffdokw22jin',
        role=RoleEnum.user,
    )
    mock_db.users.get_user_with_hashed_password = AsyncMock(return_value=mock_user)
    mock_db.commit = AsyncMock()
    service = AuthService(mock_db)
    service.verify_password = lambda p, h: password_correct
    service.create_access_token = lambda uid: {'access_token': 'tokengjdiokfgzjhnb'}

    if expected_exception:
        with pytest.raises(expected_exception):
            await service.login_and_get_access_token(data)
    else:
        response = await service.login_and_get_access_token(data)
        assert 'access_token' in response
        token = response["access_token"]
        assert token != ""


@pytest.mark.asyncio
@pytest.mark.parametrize("uid", [
    (1),
    (2),
    (3)
])
async def test_get_one_or_none_user(uid):
    mock_db = AsyncMock()
    mock_user = User(
        id=uid,
        first_name='John',
        last_name='Doe',
        birth_day=date(2005, 12, 2),
        nickname='alexmercer',
        email='johndoe2005@gmail.com',
        role=RoleEnum.user,
    )
    mock_db.users.get_one_or_none = AsyncMock(return_value=mock_user)

    service = AuthService(mock_db)

    user = await service.get_one_or_none_user(uid)
    assert user is not None
    assert user.id == uid