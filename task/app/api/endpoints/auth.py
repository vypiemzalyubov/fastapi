from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate
from app.db.database import get_async_session
from app.repositories.user_repository import UserRepository, SqlAlchemyUserRepository
from app.utils.utils import verify_password

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

security = HTTPBasic()


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUserRepository(session)


async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_user(username=credentials.username)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


@auth_router.post("/login")
async def login_user(user: UserCreate = Depends(authenticate_user)):
    return user
