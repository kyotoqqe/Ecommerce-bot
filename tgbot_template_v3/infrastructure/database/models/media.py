from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from .base import Base, TableNameMixin, TimestampMixin
from typing import Optional
from enum import Enum

from aiogram.types import PhotoSize, Video


class MediaType(Enum):
    photo = PhotoSize
    video = Video


class Media(Base, TableNameMixin, TimestampMixin):
    media_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    telegram_media_id: Mapped[int] = mapped_column(
        String(255), unique=True)
    media_type: Mapped[MediaType]
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"))
    alt_text: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, default="Изображение карточки товара")
    is_feature: Mapped[bool] = mapped_column(default=False, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="medias")
