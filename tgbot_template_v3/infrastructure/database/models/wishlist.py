
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin


class WishlistProducts(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    wishlist_id: Mapped[int] = mapped_column(
        ForeignKey("wishlist.wishlist_id"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id"))

    wishlist: Mapped["Wishlist"] = relationship(
        back_populates="wishlist_products")
    products: Mapped["Product"] = relationship(back_populates="wishlisted_by")


class Wishlist(Base, TableNameMixin):
    wishlist_id: Mapped[int] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(back_populates="wishlist")
    wishlist_products: Mapped[list["WishlistProducts"]
                              ] = relationship(back_populates="wishlist")
