from src.db import Product, StoreProduct
from sqlalchemy import select
from sqlalchemy.orm import Session


class ProductService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_store_products(self, store_id: str):
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
        rows = self.session.execute(query).all()
        return map(
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
