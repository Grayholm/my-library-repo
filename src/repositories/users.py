from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.users import UserModel
from src.repositories.base import BaseRepository
from src.repositories.books import BooksRepository
from src.repositories.mappers.mappers import UserWithHashedPasswordDataMapper, UserDataMapper


class UsersRepository(BaseRepository):
    model = UserModel
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, user_email: EmailStr):
        query = select(self.model).filter_by(email=user_email)
        result = await self.session.execute(query)
        sth = result.scalar_one()

        return UserWithHashedPasswordDataMapper.map_to_domain_entity(sth)

    async def get_favorite_books(self, user_id: int):
        query = select(self.model).where(self.model.id == user_id).options(selectinload(self.model.favorites))

        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        books = user.favorites
        books = BooksRepository.mapper.map_to_domain_entity(books)
        return books