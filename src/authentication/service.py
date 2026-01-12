from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.schemas import AuthRegisterIn, AuthRegisterInternal, TokensOut, RefreshTokenInternal, \
    AuthLoginIn, LogoutAllOut, LogoutOut
from src.authentication.utils.auth_utils import is_valid_create_user_data
from src.authentication.utils.security import hash_password, verify_password
from src.authentication.utils.token_utils import create_access_token, create_refresh_token, hash_refresh_token, \
    get_token_expires_at
from src.exceptions.auth_exceptions import InvalidCredentialsException, EmailAlreadyExistsException
from src.exceptions.base_exceptions import FailedActionException
from src.exceptions.token_exceptions import InvalidTokenException, TokenRevokedException, TokenExpiredException
from src.models.models import User
from src.repositories.refresh_token_repository import TokenRepository
from src.user.repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user_repo = UserRepository(session)
        self._token_repo = TokenRepository(session)

    async def register_user(
        self,
        user_in: AuthRegisterIn,
    ) -> TokensOut:
        is_valid_create_user_data(user_in)

        if await self._user_repo.exists_user_with_email(user_in.email):
            raise EmailAlreadyExistsException()

        hashed_password = hash_password(user_in.password)
        auth_internal = AuthRegisterInternal(
            email=user_in.email,
            name=user_in.name,
            hashed_password=hashed_password,
        )

        user = await self._user_repo.create_user(
            user_in=auth_internal,
            returning_columns=User.get_pk_columns()
        )

        refresh_token = create_refresh_token()
        refresh_token_hash = hash_refresh_token(refresh_token)
        token_data = RefreshTokenInternal(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=get_token_expires_at(),
            # device_fingerprint=device_fingerprint
        )
        is_created = await self._token_repo.create_refresh_token(token_data)
        if not is_created:
            raise FailedActionException(action="Create refresh token")
        await self._session.commit()
        return TokensOut(
            access_token=create_access_token(user.id),
            refresh_token=refresh_token
        )

    async def login_user(
            self,
            user_in: AuthLoginIn,
    ) -> TokensOut:
        user = await self._user_repo.get_user_by_email(
            email=user_in.email,
            selected_columns=[User.id, User.hashed_password]
        )

        if not user or not verify_password(user_in.password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token(user.id)

        refresh_token = create_refresh_token()
        refresh_token_hash = hash_refresh_token(refresh_token)

        await self._token_repo.create_refresh_token(
            RefreshTokenInternal(
                user_id=user.id,
                token_hash=refresh_token_hash,
                expires_at=get_token_expires_at(),
            )
        )

        await self._session.commit()

        return TokensOut(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    async def login_oauth2(
            self,
            username: str,
            password: str,
    ):
        return await self.login_user(AuthLoginIn(
            email=username,
            password=password,
        ))

    async def refresh_tokens(
            self,
            token_in: str,
            device_fingerprint: str | None = None,
    ) -> TokensOut:
        if not token_in:
            raise InvalidTokenException()
        token_hash = hash_refresh_token(token_in)

        token = await self._token_repo.get_token_by_hash(token_hash, scalar=True)

        if token is None:
            raise InvalidTokenException()
        if token.revoked_at is not None:
            raise TokenRevokedException()

        if token.expires_at <= datetime.now(timezone.utc):
            raise TokenExpiredException()

        await self._token_repo.revoke_token(token.id)

        new_access_token = create_access_token(token.user_id)

        new_refresh_token = create_refresh_token()
        new_refresh_token_hash = hash_refresh_token(new_refresh_token)

        await self._token_repo.create_refresh_token(
            RefreshTokenInternal(
                user_id=token.user_id,
                token_hash=new_refresh_token_hash,
                expires_at=get_token_expires_at(),
                # device_fingerprint=device_fingerprint or token.device_fingerprint,
            )
        )

        await self._session.commit()

        return TokensOut(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def logout_user(
            self,
            token_in: str,
    ) -> LogoutOut:

        if not token_in:
            raise InvalidTokenException()
        token_hash = hash_refresh_token(token_in)

        is_revoked = await self._token_repo.revoke_token_by_hash(token_hash)

        if not is_revoked:
            raise InvalidTokenException()

        await self._session.commit()

        return LogoutOut(
            device_logged_out=is_revoked,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    async def logout_all_devices(
            self,
            token_in: str,
    ) -> LogoutAllOut:

        if not token_in:
            raise InvalidTokenException()
        token_hash = hash_refresh_token(token_in)

        token_record = await self._token_repo.get_token_by_hash(token_hash, scalar=True)
        if not token_record:
            raise InvalidTokenException()

        user_id = token_record.user_id
        revoked_count = await self._token_repo.revoke_tokens_by_user_id(user_id)
        await self._session.commit()

        return LogoutAllOut(
            devices_logged_out=revoked_count,
            timestamp=datetime.now(timezone.utc).isoformat()
        )