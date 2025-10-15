from typing import Annotated

from fastapi import Depends

from src.core.db import async_session_maker
from src.core.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]