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
