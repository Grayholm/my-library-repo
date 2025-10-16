from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    description: str | None = None
    file_path: str = Field(...)
    author_id: int = Field(...)
    uploader: int = Field(...)
    authors: list[str] | None = None
    reviews: list[str] | None = None
    fans: list[str] | None = None