from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import (
    TIMESTAMP,
    UUID,
    ForeignKey,
    Column,
    Integer,
    Text,
)


class Base(DeclarativeBase):
    pass


class Store(Base):
    __tablename__ = "stores"
    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[str] = Column(TIMESTAMP, nullable=False)
    updated_at: Mapped[str] = Column(TIMESTAMP, nullable=False)
    deleted_at: Mapped[str | None] = Column(TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = Column(Text, nullable=False)
    price: Mapped[int] = Column(Integer, nullable=False)
    description: Mapped[str] = Column(Text, nullable=True)
    image_url: Mapped[str] = Column(Text, nullable=True)
    created_at: Mapped[str] = Column(TIMESTAMP, nullable=False)
    updated_at: Mapped[str] = Column(TIMESTAMP, nullable=False)
    deleted_at: Mapped[str | None] = Column(TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class StoreProduct(Base):
    __tablename__ = "stores_products"
    store_id: Mapped[str] = Column(
        UUID(as_uuid=True), ForeignKey("store.id"), primary_key=True
    )
    product_id: Mapped[str] = Column(
        UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    )
    category: Mapped[str] = Column(Text, nullable=False)
    position: Mapped[int] = Column(Integer, nullable=False)
