from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate
from app.db.models import User

from app.utils.utils import hash_pass


class UserRepository(ABC):

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass


class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = await self.session.execute(select(User).filter(User.id == user_id))
        return stmt.scalar()

    async def create_user(self, user: UserCreate) -> User:
        hashed_pass = hash_pass(user.password)
        user.password = hashed_pass
        stmt = User(**user.model_dump())
        self.session.add(stmt)
        await self.session.commit()
        await self.session.refresh(stmt)
        return stmt

    async def update_user(self, user_id: int, user: UserCreate) -> User:
        hashed_pass = hash_pass(user.password)
        user.password = hashed_pass
        stmt = await self.get_user(user_id)
        if stmt:
            for key, value in user.model_dump().items():
                setattr(stmt, key, value)
            await self.session.commit()
            await self.session.refresh(stmt)
            return stmt
        return None

    async def delete_user(self, user_id: int) -> None:
        stmt = await self.get_user(user_id)
        if stmt:
            await self.session.delete(stmt)
            await self.session.commit()
            return stmt
        return None
