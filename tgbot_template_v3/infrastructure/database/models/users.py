from typing import Optional

from sqlalchemy import String, BIGINT, Integer, Boolean, ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, TableNameMixin


class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a User in the application.
    If you want to learn more about SQLAlchemy and Alembic, you can check out the following link to my course:
    https://www.udemy.com/course/sqlalchemy-alembic-bootcamp/?referralCode=E9099C5B5109EB747126

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        username (Mapped[Optional[str]]): The username of the user.
        full_name (Mapped[str]): The full name of the user.
        active (Mapped[bool]): Indicates whether the user is active or not.
        language (Mapped[str]): The language preference of the user.

    Methods:
        __repr__(): Returns a string representation of the User object.

    Inherited Attributes:
        Inherits from Base, TimestampMixin, and TableNameMixin classes, which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, TimestampMixin, and TableNameMixin classes, which provide additional functionality.

    """
    user_id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True)
    full_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, server_default=false())
    wishlist_id: Mapped[int] = mapped_column(
        ForeignKey("wishlist.wishlist_id", ondelete="SET NULL"), nullable=True)

    wishlist: Mapped["Wishlist"] = relationship(back_populates="user")
    referrers_user: Mapped[list["Referal"]] = relationship(
        back_populates="referrers")
    refers_user: Mapped[list["Referal"]] = relationship(
        back_populates="refers")

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.full_name}>"


class Referal(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    referrers_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"))
    refers_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"))

    referrers: Mapped["User"] = relationship(back_populates="referrers_user")
    refers: Mapped["User"] = relationship(back_populates="refers_user")
