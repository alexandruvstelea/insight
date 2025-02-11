from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from ...config import settings
from ...database.main import get_session
from ...database.models.user import User
from .schemas import UserOut
from fastapi import Cookie, HTTPException
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(
    plain_password: str, hashed_password: str, password_context: CryptContext
):
    try:
        logger.info("Verifying password.")
        return password_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"An unexpected error has occured while verifying password:\n{e}")
        raise e


def create_access_token(user_email: str, expires_delta: int) -> str:
    try:
        logger.info(f"Creating access token for user with email {user_email}.")
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        to_encode = {"sub": user_email, "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
        )
        if encoded_jwt:
            logger.info(
                f"Successfully created access token for user with email {user_email}."
            )
            return encoded_jwt
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while creating token for user with email {user_email}:\n{e}"
        )
        raise e


def get_password_hash(password: str, password_context: CryptContext) -> str:
    return password_context.hash(password)


def user_to_out(user: User) -> UserOut:
    logger.info(f"Converting user with email {user.email} to UserOut format.")
    return UserOut(
        id=user.id,
        email=user.email,
        role=user.role,
        professor_id=user.professor_id,
    )


def decode_jwt(token: str = Depends(oauth2_scheme)):
    try:
        logger.info("Decoding JWT token.")
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )
        return payload
    except JWTError as e:
        logger.error(f"A JWT error has occured while retrieving current user:\n{e}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="An error has occured while retrieving current user.",
        )


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    access_token: str = Cookie(None)

) -> UserOut:
    try:
        logger.info("Retrieving current user.")
        if not access_token:
            logger.error("No token found in cookies.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="No valid token provided.",
            )

        payload = decode_jwt(access_token)
        user_email: str = payload.get("sub")
        if not user_email:
            logger.error("Invalid token provided.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token provided.",
            )
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.error("Invalid token provided.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token provided.",
            )
        logger.info(f"Successfully retrieved current user with email {user.email}.")
        return user_to_out(user)
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while getting current user:\n{e}"
        )
        raise e
    
async def get_current_user_no_cookie(
    session: AsyncSession = Depends(get_session),
    access_token: str = Depends(oauth2_scheme)

) -> UserOut:
    try:
        logger.info("Retrieving current user.")
        if not access_token:
            logger.error("No token found in cookies.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="No valid token provided.",
            )

        payload = decode_jwt(access_token)
        user_email: str = payload.get("sub")
        if not user_email:
            logger.error("Invalid token provided.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token provided.",
            )
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.error("Invalid token provided.")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token provided.",
            )
        logger.info(f"Successfully retrieved current user with email {user.email}.")
        return user_to_out(user)
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while getting current user:\n{e}"
        )
        raise e
