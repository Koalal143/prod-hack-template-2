from datetime import timedelta
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.core.error import ConflictError, NotFoundError, AccessError
from src.models.users import User
from src.services.users import UserService
from src.schemas.users import UserCreateSchema, UserLoginSchema


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(mock_user_repo)


@pytest.mark.asyncio
async def test_register_user(user_service, mock_user_repo, monkeypatch):
    mock_user = User(id=1, email="test3@example.com")
    mock_user_repo.create.return_value = mock_user
    monkeypatch.setattr("src.services.users.get_password_hash", lambda _: "hashed_password")
    create_token_mock = MagicMock(return_value="test_token")
    monkeypatch.setattr("src.services.users.create_token", create_token_mock)

    user_create = UserCreateSchema(email="test3@example.com", password="password1234ASD.", first_name="test", second_name="test")
    user, token = await user_service.register(user_create)

    assert user.email == "test3@example.com"
    assert token == "test_token"
    mock_user_repo.create.assert_called_once()
    create_token_mock.assert_called_once_with(
        data={"sub": "test3@example.com"}, expires_delta=timedelta(hours=7)
    )


@pytest.mark.asyncio
async def test_register_user_conflict(user_service, mock_user_repo, monkeypatch):
    mock_user_repo.create.side_effect = ConflictError
    monkeypatch.setattr("src.services.users.get_password_hash", lambda _: "hashed_password")

    user_create = UserCreateSchema(email="test@example.com", password="password1234ASD.", first_name="test", second_name="test")

    with pytest.raises(ConflictError):
        await user_service.register(user_create)


@pytest.mark.asyncio
async def test_login_user(user_service, mock_user_repo, monkeypatch):
    mock_user = User(id=1, email="test@example.com", password_hash="hashed_password")
    mock_user_repo.get_by_email.return_value = mock_user
    monkeypatch.setattr("src.services.users.verify_password", lambda p, h: True)
    create_token_mock = MagicMock(return_value="test_token")
    monkeypatch.setattr("src.services.users.create_token", create_token_mock)

    user_login = UserLoginSchema(email="test@example.com", password="password")
    token = await user_service.login(user_login)

    assert token == "test_token"
    create_token_mock.assert_called_once_with(
        data={"sub": "test@example.com"}, expires_delta=timedelta(hours=7)
    )


@pytest.mark.asyncio
async def test_login_user_not_found(user_service, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None

    user_login = UserLoginSchema(email="test@example.com", password="password")

    with pytest.raises(NotFoundError):
        await user_service.login(user_login)


@pytest.mark.asyncio
async def test_login_user_access_error(user_service, mock_user_repo, monkeypatch):
    mock_user = User(id=1, email="test@example.com", password_hash="hashed_password")
    mock_user_repo.get_by_email.return_value = mock_user
    monkeypatch.setattr("src.services.users.verify_password", lambda p, h: False)

    user_login = UserLoginSchema(email="test@example.com", password="password")

    with pytest.raises(AccessError):
        await user_service.login(user_login)
