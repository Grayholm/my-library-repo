from src.models.books import BookModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookDataMapper


class BooksRepository(BaseRepository):
    model = BookModel
    mapper = BookDataMapper

