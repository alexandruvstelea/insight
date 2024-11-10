from ...database.main import get_session
from fastapi import APIRouter, Depends, Header, Response
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import UserIn, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import UserOperations
from http import HTTPStatus
from ...utility.authorizations import authorize
from typing import Dict, List
from .utils import get_current_user, get_current_user_no_cookie

from fastapi_limiter.depends import RateLimiter
import logging

from ...config import settings

logger = logging.getLogger(__name__)
users_router = APIRouter(prefix="/api/users")


@users_router.get(
    "/",
    response_model=List[UserOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_users(
    professor_id: int = None,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[UserOut]:
    logger.info(f"Received GET request on endpoint /api/users from IP {client_ip}.")
    users = await UserOperations(session).get_users(professor_id)
    return users


@authorize(role=["admin", "professor", "student"])
@users_router.get(
    "/current",
    response_model=dict,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_current(
    client_ip: str = Header(None, alias="X-Real-IP"),
    current_user: dict = Depends(get_current_user_no_cookie),
) -> dict:
    logger.info(
        f"Received GET request on endpoint /api/users/current from IP {client_ip}."
    )
    return {
        "current_user": current_user,
    }


@users_router.post(
    "/token",
    response_model=Dict,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    logger.info(
        f"Received POST request on endpoint /api/users/token from IP {client_ip}."
    )
    token = await UserOperations(session).authenticate_user(
        form_data.username, form_data.password
    )
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=False,
        samesite="None",
        # secure=True
        # samesite="Strict",
        # domain=".insightbv.ro",
        max_age=60 * settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return {"message": "Login successful"}


@authorize(role=["admin"])
@users_router.post(
    "/register",
    response_model=UserOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def register_user(
    user_data: UserIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> UserOut:
    logger.info(
        f"Received POST request on endpoint /api/users/register from IP {client_ip}."
    )
    user = await UserOperations(session).create_user(user_data)
    return user


@authorize(role=["admin"])
@users_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_user(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/users/{id} from IP {client_ip}."
    )
    result = await UserOperations(session).delete_user(id)
    return result
