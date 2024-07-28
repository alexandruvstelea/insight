from sqlalchemy import select
from ...database.models.user import User
from .schemas import UserIn, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus
from ...utility.error_parsing import format_integrity_error
from passlib.context import CryptContext
from ...config import settings
from .utils import verify_password, create_access_token, get_password_hash, user_to_out
import logging
from typing import List

logger = logging.getLogger(__name__)


class UserOperations:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_users(self, professor_id: int) -> List[UserOut]:
        try:
            if professor_id:
                logger.info(
                    f"Retrieving all users with professor ID {professor_id} from database."
                )
                query = select(User).where(User.professor_id == professor_id)
            else:
                logger.info("Retrieving all users from database.")
                query = select(User)
            result = await self.session.execute(query)
            users = result.scalars().unique().all()
            if users:
                logger.info("Succesfully retrieved all users from database.")
                return [
                    user_to_out(users)
                    for user in sorted(list(users), key=lambda x: x.email)
                ]
            logger.error("No users found.")
            raise HTTPException(status_code=404, detail="No users found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving users:\n{e}"
            )
            raise e

    async def authenticate_user(self, email: str, password: str) -> dict:
        try:
            logger.info(f"Authenticating user with email {email}.")
            if email and password:
                query = select(User).where(User.email == email)
                result = await self.session.execute(query)
                user = result.scalars().first()
                if not user or not verify_password(
                    password, user.password, self.password_context
                ):
                    logger.error("The provided credentials are not valid.")
                    raise HTTPException(
                        status_code=HTTPStatus.UNAUTHORIZED,
                        detail="The provided credentials are not valid.",
                    )
                access_token = create_access_token(
                    user.email, settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
                )
                if access_token:
                    logger.info(
                        f"Successfully authenticated user with email {user.email}."
                    )
                    return {"access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while trying to authenticate user with email {email}:\n{e}"
            )
            raise e

    async def create_user(self, user: UserIn) -> UserOut:
        try:
            logger.info(
                f"Creating new user with email {user.email} and role {user.role}"
            )
            query = select(User).where(User.email == user.email)
            result = await self.session.execute(query)
            existing_user = result.scalars().all()
            if existing_user:
                logger.error(f"An user with email {user.email} already exists.")
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"An user with email {user.email} already exists.",
                )
            hashed_password = get_password_hash(user.password, self.password_context)
            new_user = User(
                email=user.email,
                password=hashed_password,
                role=user.role,
            )
            if user.professor_id:
                new_user.professor_id = user.professor_id
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            logger.info("Succesfully added new user to database.")
            return user_to_out(new_user)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding user to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_user(self, id: int):
        try:
            logger.info(f"Deleting user with ID {id}.")
            user = await self.session.get(User, id)
            if user:
                await self.session.delete(user)
                await self.session.commit()
                logger.info(f"Succesfully deleted user with ID {id}.")
                return JSONResponse(f"User with ID {id} deleted.")
            logger.error(f"No user with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No user with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting user with ID {id}:\n{e}"
            )
            raise e
