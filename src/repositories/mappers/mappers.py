from src.models.books import BookModel
from src.models.users import UserModel
from src.repositories.mappers.base import DataMapper
from src.schemas.books import Book
from src.schemas.users import User, UserWithHashedPassword


class UserDataMapper(DataMapper):
    db_model = UserModel
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UserModel
    schema = UserWithHashedPassword

class BookDataMapper(DataMapper):
    db_model = BookModel
    schema = Book