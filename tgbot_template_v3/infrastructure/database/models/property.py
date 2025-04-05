from sqlalchemy import String,   ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base, TableNameMixin, TimestampMixin


class PropertyName(Base, TableNameMixin, TimestampMixin):
    property_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)

    descriptions: Mapped[list["Property"]
                         ] = relationship(back_populates="name")


class Property(Base, TableNameMixin, TimestampMixin):
    description_id: Mapped[int] = mapped_column(
        primary_key=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    property_id: Mapped[int] = mapped_column(
        ForeignKey("propertyname.property_id", ondelete="CASCADE"))

    name: Mapped["PropertyName"] = relationship(back_populates="descriptions")

    products: Mapped[list["Product"]] = relationship(
        back_populates="properties", secondary="productproperties")
