from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate, UserFromDB
from app.db.database import get_async_session
from app.repositories.user_repository import UserRepository, SqlAlchemyUserRepository
from app.api.endpoints.auth import authenticate_user

user_router = APIRouter(
    prefix="/users",
    tags=["User"]
)


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return SqlAlchemyUserRepository(session)


@user_router.get("/", response_model=list[UserFromDB])
async def get_users(repo: UserRepository = Depends(get_user_repository),
                    auth: UserCreate = Depends(authenticate_user)):
    result = await repo.get_users()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"
        )
    return result


@user_router.post("/add_user", response_model=UserFromDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate,
                      repo: UserRepository = Depends(get_user_repository)):
    result = await repo.create_user(user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    return result


@user_router.post("/change_user", response_model=UserFromDB)
async def update_user(user_id: int,
                      user: UserCreate,
                      repo: UserRepository = Depends(get_user_repository),
                      auth: UserCreate = Depends(authenticate_user)):
    result = await repo.update_user(user_id, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      repo: UserRepository = Depends(get_user_repository),
                      auth: UserCreate = Depends(authenticate_user)):
    result = await repo.delete_user(user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
