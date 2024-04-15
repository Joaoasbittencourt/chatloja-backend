from uuid import uuid4
from sqlalchemy import (
    MetaData,
    TIMESTAMP,
    UUID,
    ForeignKey,
    Column,
    Integer,
    Table,
    Text,
)


metadata = MetaData()

stores_table = Table(
    "stores",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", Text, nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("updated_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP, nullable=True),
)

products_table = Table(
    "products",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", Text, nullable=False),
    Column("price", Integer, nullable=False),
    Column("description", Text, nullable=True),
    Column("image_url", Text, nullable=True),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("updated_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP, nullable=True),
)

stores_products_table = Table(
    "stores_products",
    metadata,
    Column("store_id", UUID(as_uuid=True), ForeignKey("stores.id"), primary_key=True),
    Column(
        "product_id", UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    ),
    Column("category", Text, nullable=False),
    Column("position", Integer, nullable=False),
)
