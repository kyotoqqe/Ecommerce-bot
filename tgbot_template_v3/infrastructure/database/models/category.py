from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from .base import Base, TableNameMixin
from typing import Optional


class Category(Base, TableNameMixin):
    category_id: Mapped[int] = mapped_column(
        primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.category_id",ondelete="SET NULL"), nullable=True)

    product: Mapped[list["Product"]] = relationship(back_populates="category")
    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[category_id], back_populates="children",)
    children: Mapped[list["Category"]] = relationship("Category",
                                                      back_populates="parent")
