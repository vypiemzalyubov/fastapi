from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate, UserFromDB
from app.db.database import get_async_session
from app.repositories.user_repository import UserRepository, SqlAlchemyUserRepository

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

security = HTTPBasic()


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUserRepository(session)


async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), repo: UserRepository = Depends(get_user_repository)):
    result = await repo.get_user(credentials.username)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


@auth_router.post("/login")
async def login_user(user: UserCreate = Depends(authenticate_user)):
    return user
