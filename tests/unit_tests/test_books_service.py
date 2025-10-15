from unittest.mock import AsyncMock
import pytest

@pytest.mark.asyncio
async def test_get_my_books():
    mock_db = AsyncMock()
    service = BooksService(mock_db)

