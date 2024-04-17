from typing import List
from pydantic import UUID4, BaseModel


class StorePath(BaseModel):
    store_id: UUID4


class StoreProductPath(StorePath):
    product_id: UUID4


class CreateProductDTO(BaseModel):
    name: str
    price: float
    imageUrl: str | None
    category: str
    description: str


class StoreProduct(BaseModel):
    id: UUID4
    name: str
    description: str
    imageUrl: str | None
    category: str
    price: int

    @staticmethod
    def from_row(row):
        return StoreProduct(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            imageUrl=row["image_url"],
            category=row["category"],
            price=row["price"],
        )


class Store(BaseModel):
    id: UUID4
    name: str

    @staticmethod
    def from_row(row):
        return Store(
            id=row["id"],
            name=row["name"],
        )


class GetStoreProductsResponse(BaseModel):
    products: List[StoreProduct]

    def __init__(self, products: List[StoreProduct]):
        super().__init__(products=products)
        self.products = products

    def to_dict(self):
        return {"products": [product.model_dump() for product in self.products]}


class GetStoresResponse(BaseModel):
    stores: List[Store]

    def __init__(self, stores: List[Store]):
        super().__init__(stores=stores)
        self.stores = stores

    def to_dict(self):
        return {"stores": [store.model_dump() for store in self.stores]}
