from decimal import Decimal
from typing import Optional

from sqlalchemy import String,  DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base, TableNameMixin, TimestampMixin


class Product(Base, TableNameMixin, TimestampMixin):
    product_id: Mapped[int] = mapped_column(
        primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    price: Mapped[Decimal] = mapped_column(
        DECIMAL, nullable=False)  # всегда больше 0
    # для скидок можно создать отдельную модель чтобы иметь группы скидок
    available: Mapped[bool] = mapped_column(default=False, nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.category_id", ondelete="SET NULL"), nullable=True)

    properties: Mapped[list["Property"]] = relationship(
        back_populates="products", secondary="productproperties")
    # comments -> тож надо придумать как обыграть без веб приложения нормальный показ достаточно проблематичен
    category: Mapped["Category"] = relationship(back_populates="product")
    feature_media: Mapped["Media"] = relationship(back_populates="product",
                                                  primaryjoin="and_(Product.product_id==Media.product_id, Media.is_feature==True)")
    medias: Mapped[list["Media"]] = relationship(back_populates="product")

    wishlisted_by: Mapped[list["WishlistProducts"]
                          ] = relationship(back_populates="products")


class ProductProperties(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey(
        "product.product_id", ondelete="CASCADE"))
    property_id: Mapped[int] = mapped_column(ForeignKey(
        "property.description_id", ondelete="CASCADE"))
