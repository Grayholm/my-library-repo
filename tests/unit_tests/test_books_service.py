import pytest
from unittest.mock import AsyncMock
from src.services.books import BooksService

@pytest.mark.parametrize(
    "user,title,author,expected_exception",
    [

    ],
)
async def test_create_book_as_admin(user, title, author, expected_exception):
    mock_db = AsyncMock()
    service = BooksService(mock_db)

    if expected_exception:
        with pytest.raises(expected_exception):
            await service.create_book(user, title, author)
    else:
        book = await service.create_book(user, title, author)
        assert book.title == title
        assert book.author == author
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()
