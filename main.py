import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy import (
    select,
    create_engine,
    TIMESTAMP,
    UUID,
    ForeignKey,
    Column,
    Integer,
    Text,
)

load_dotenv()


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


engine = create_engine(os.environ["DB_CONNECTION"])
session = Session(engine)
engine.connect()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.get("/stores")
def list_stores():
    try:
        result = session.scalars(select(Store))
        rows = result.all()
        return list(map(lambda row: row.to_dict(), rows))
    except Exception as e:
        return {"error": str(e)}


@app.get("/stores/<uuid:store_id>")
def get_store_and_products(store_id):
    try:
        store = session.get(Store, store_id)
        print(store)
        if store is None:
            return {"error": "Store not found"}, 404

        return store.to_dict(), 200
    except Exception as e:
        return {"error": str(e)}, 400


@app.get("/stores/<uuid:store_id>/products")
def list_products(store_id):
    try:
        query = (
            select(
                Product.id,
                Product.name,
                Product.price,
                Product.image_url,
                StoreProduct.category,
                Product.description,
            )
            .select_from(StoreProduct)
            .where(StoreProduct.store_id == store_id)
            .join(Product, StoreProduct.product_id == Product.id)
            .order_by(StoreProduct.position)
        )
        rows = session.execute(query).all()
        mapped = map(
            lambda row: {
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "imageUrl": row[3],
                "category": row[4],
                "description": row[5],
            },
            rows,
        )

        return list(mapped)
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400
