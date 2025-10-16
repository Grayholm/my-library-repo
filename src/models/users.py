import enum
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Enum, Column, ForeignKey, Table, Text

from src.core.db import Base


class RoleEnum(enum.Enum):
    user = "user"
    author = "author"
    admin = "admin"

favorite_books = Table(
    "favorite_books",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)

book_authors_books = Table(
    "book_authors_books",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("book_authors.id"), primary_key=True),
)

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    nickname: Mapped[str] = mapped_column(String(100), unique=True)
    birth_day: Mapped[date] = mapped_column(Date())
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.user)

    uploaded_books: Mapped[list["BookModel"]] = relationship(back_populates="uploader")
    reviews: Mapped[list["ReviewModel"]] = relationship(back_populates="user")
    favorites: Mapped[list["BookModel"]] = relationship(
        "BookModel", secondary=favorite_books, back_populates="fans"
    )

class BookAuthorModel(Base):
    __tablename__ = "book_authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    birth_year: Mapped[int | None]
    death_year: Mapped[int | None]
    bio: Mapped[str | None] = mapped_column(Text)

    books: Mapped[list["BookModel"]] = relationship(
        secondary=book_authors_books, back_populates="authors"
    )