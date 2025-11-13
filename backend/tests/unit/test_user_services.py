import uuid
from datetime import timedelta, datetime, UTC
from unittest.mock import AsyncMock, patch

import pytest

from src.core.error import AccessError, ConflictError, NotFoundError
from src.core.security import create_token, get_string_hash
from src.models.tokens import RefreshToken
from src.models.users import User
from src.schemas.tokens import TokenReadSchema
from src.schemas.users import UserCreateSchema, UserLoginSchema, UserRegisterSchema, UserReadSchema
from src.services.users import UserService
from src.settings import settings


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.fixture
def mock_token_repo():
    return AsyncMock()


@pytest.fixture
def user_service(mock_user_repo, mock_token_repo):
    return UserService(mock_user_repo, mock_token_repo)


@pytest.mark.asyncio
async def test_register_user(user_service, mock_user_repo, mock_token_repo):
    mock_user = User(id=1, email="test@example.com", first_name="test", second_name="test")
    mock_user_repo.create.return_value = mock_user
    user_create = UserCreateSchema(email="test@example.com", password="passwordSDf123.", first_name="test", second_name="test")

    with patch("src.services.users.get_string_hash", return_value="hashed_password"):
        result = await user_service.register(user_create)

        assert isinstance(result, UserRegisterSchema)
        assert isinstance(result.user, UserReadSchema)
        assert isinstance(result.tokens, TokenReadSchema)
        assert result.user.email == "test@example.com"
        assert result.tokens.access_token
        assert result.tokens.refresh_token

        mock_user_repo.create.assert_called_once()
        mock_token_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_conflict(user_service, mock_user_repo):
    mock_user_repo.create.side_effect = ConflictError
    user_create = UserCreateSchema(email="test@example.com", password="passwordSDf123.", first_name="test", second_name="test")

    with patch("src.services.users.get_string_hash", return_value="hashed_password"):
        with pytest.raises(ConflictError):
            await user_service.register(user_create)


@pytest.mark.asyncio
async def test_login_user(user_service, mock_user_repo, mock_token_repo):
    mock_user = User(id=1, email="test@example.com", password_hash="hashed_password")
    mock_user_repo.get_by_email.return_value = mock_user
    user_login = UserLoginSchema(email="test@example.com", password="passwordSDf123.")

    with patch("src.services.users.verify_hash", return_value=True):
        result = await user_service.login(user_login)

        assert isinstance(result, TokenReadSchema)
        assert result.access_token
        assert result.refresh_token

        mock_user_repo.get_by_email.assert_called_once_with("test@example.com")
        mock_token_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_login_user_not_found(user_service, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None
    user_login = UserLoginSchema(email="test@example.com", password="password")

    with pytest.raises(NotFoundError):
        await user_service.login(user_login)


@pytest.mark.asyncio
async def test_login_user_access_error(user_service, mock_user_repo):
    mock_user = User(id=1, email="test@example.com", password_hash="hashed_password")
    mock_user_repo.get_by_email.return_value = mock_user
    user_login = UserLoginSchema(email="test@example.com", password="password")

    with patch("src.services.users.verify_hash", return_value=False):
        with pytest.raises(AccessError):
            await user_service.login(user_login)


@pytest.mark.asyncio
async def test_refresh_token_success(user_service, mock_user_repo, mock_token_repo):
    user_email = "test@example.com"
    token_id = str(uuid.uuid4())
    refresh_token = create_token(
        data={"sub": user_email, "id": token_id},
        expires_delta=timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
        token_type="refresh"
    )
    hashed_token = get_string_hash(refresh_token)

    mock_user = User(id=1, email=user_email)
    mock_token = RefreshToken(id=token_id, token_hash=hashed_token)

    mock_user_repo.get_by_email.return_value = mock_user
    mock_token_repo.get.return_value = mock_token

    with patch("src.services.users.verify_hash", return_value=True):
        result = await user_service.refresh_token(refresh_token)

        assert isinstance(result, TokenReadSchema)
        assert result.refresh_token != refresh_token
        assert result.access_token

        mock_token_repo.delete.assert_called_once_with(mock_token)
        mock_token_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_refresh_token_invalid_token(user_service):
    with pytest.raises(AccessError):
        await user_service.refresh_token("invalid_token")


@pytest.mark.asyncio
async def test_refresh_token_wrong_type(user_service):
    access_token = create_token(
        data={"sub": "test@example.com"},
        expires_delta=timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME),
        token_type="access"
    )
    with pytest.raises(AccessError):
        await user_service.refresh_token(access_token)


@pytest.mark.asyncio
async def test_refresh_token_expired(user_service, mock_user_repo, mock_token_repo):
    user_email = "test@example.com"
    token_id = str(uuid.uuid4())
    
    # Create an expired token
    expired_delta = timedelta(seconds=-1)
    refresh_token = create_token(
        data={"sub": user_email, "id": token_id},
        expires_delta=expired_delta,
        token_type="refresh"
    )
    
    with pytest.raises(AccessError):
        await user_service.refresh_token(refresh_token)


@pytest.mark.asyncio
async def test_refresh_token_not_in_db(user_service, mock_user_repo, mock_token_repo):
    user_email = "test@example.com"
    token_id = str(uuid.uuid4())
    refresh_token = create_token(
        data={"sub": user_email, "id": token_id},
        expires_delta=timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
        token_type="refresh"
    )

    mock_user = User(id=1, email=user_email)
    mock_user_repo.get_by_email.return_value = mock_user
    mock_token_repo.get.return_value = None

    with pytest.raises(AccessError):
        await user_service.refresh_token(refresh_token)


@pytest.mark.asyncio
async def test_get_user_by_access_token_success(user_service, mock_user_repo):
    user_email = "test@example.com"
    access_token = create_token(
        data={"sub": user_email},
        expires_delta=timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME),
        token_type="access"
    )
    mock_user = User(id=1, email=user_email)
    mock_user_repo.get_by_email.return_value = mock_user

    user = await user_service.get_user_by_access_token(access_token)
    assert user == mock_user


@pytest.mark.asyncio
async def test_get_user_by_access_token_invalid(user_service):
    with pytest.raises(AccessError):
        await user_service.get_user_by_access_token("invalid_token")


@pytest.mark.asyncio
async def test_get_user_by_access_token_wrong_type(user_service):
    refresh_token = create_token(
        data={"sub": "test@example.com", "id": str(uuid.uuid4())},
        expires_delta=timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME),
        token_type="refresh"
    )
    with pytest.raises(AccessError):
        await user_service.get_user_by_access_token(refresh_token)
