from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate, UserFromDB
from app.db.models import User
from app.utils.utils import hash_password


class UserRepository(ABC):

    @abstractmethod
    async def get_user(self, **kwargs) -> User:
        pass

    @abstractmethod
    async def get_users(self, user_id: int) -> list[UserFromDB]:
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

    async def get_user(self, **kwargs) -> User:
        stmt = await self.session.execute(select(User).filter_by(**kwargs))
        return stmt.scalar()

    async def get_users(self) -> list[UserFromDB]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def create_user(self, user: UserCreate) -> User:
        stmt = await self.get_user(username=user.username, email=user.email)
        if stmt is None:
            hashed_pass = hash_password(user.password)
            user.password = hashed_pass
            stmt = User(**user.model_dump())
            self.session.add(stmt)
            await self.session.commit()
            await self.session.refresh(stmt)
            return stmt
        return None

    async def update_user(self, user_id: int, user: UserCreate) -> User:
        stmt = await self.get_user(id=user_id)
        if stmt:
            hashed_pass = hash_password(user.password)
            user.password = hashed_pass
            for key, value in user.model_dump().items():
                setattr(stmt, key, value)
            await self.session.commit()
            await self.session.refresh(stmt)
            return stmt
        return None

    async def delete_user(self, user_id: int) -> None:
        stmt = await self.get_user(id=user_id)
        if stmt:
            await self.session.delete(stmt)
            await self.session.commit()
            return stmt
        return None
