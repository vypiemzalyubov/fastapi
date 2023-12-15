from fastapi import APIRouter, status
from app.db.database import CRUD
from app.models.schemas import UserCreate, UserGet


router = APIRouter(
    prefix="/v1"
)


@router.post("/users/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    result = await CRUD.create_in_db(user)
    return result


@router.get("/users/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):  # -> Any:
    result = await CRUD.get_from_db(user_id)
    return result


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    result = await CRUD.delete_from_db(user_id)
    return result
