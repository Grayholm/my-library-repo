from fastapi import APIRouter

from src.utils.auth_utils import UserIdDep

router = APIRouter(prefix="/books", tags=["Библиотека"])

@router.post()
async def create_book(user: UserIdDep, data):
    pass