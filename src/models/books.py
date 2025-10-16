from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.models.reviews import ReviewModel
from src.models.users import BookAuthorModel, book_authors_books, UserModel, favorite_books


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    uploader: Mapped["UserModel"] = relationship(back_populates="uploaded_books")
    reviews: Mapped[list["ReviewModel"]] = relationship(back_populates="book")
    authors: Mapped[list["BookAuthorModel"]] = relationship(
        secondary=book_authors_books, back_populates="books"
    )
    fans: Mapped[list["UserModel"]] = relationship(
        "User", secondary=favorite_books, back_populates="favorites"
    )