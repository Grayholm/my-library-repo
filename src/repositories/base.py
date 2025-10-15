from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session