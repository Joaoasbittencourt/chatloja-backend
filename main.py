from http import HTTPStatus
from src.dto import (
    CreateProductDTO,
    GetStoreProductsResponse,
    GetStoresResponse,
    Store,
    StoreProduct,
    StorePath,
    StoreProductPath,
)
from src.services import (
    create_store_product,
    delete_store_product,
    get_store,
    get_store_products,
    get_stores,
)
from src.errors import NotFoundException
from src.state import AppState

ctx = AppState()
app = ctx.app


@app.get(
    "/stores/<uuid:store_id>", responses={200: Store}, description="Get a store by id"
)
def get_store_handler(path: StorePath):
    with ctx.engine.connect() as conn:
        store = get_store(conn, path.store_id)
        if store is None:
            raise NotFoundException(f"Store {path.store_id} not found")
        response = Store.from_row(store)
        return response.model_dump(), HTTPStatus.OK


@app.get("/stores", responses={200: GetStoresResponse}, description="Get all stores")
def get_stores_handler():
    with ctx.engine.connect() as conn:
        rows = get_stores(conn)
        stores = map(Store.from_row, rows)
        response = GetStoresResponse(list(stores))
        return response.to_dict(), HTTPStatus.OK


@app.get(
    "/stores/<uuid:store_id>/products",
    responses={200: GetStoreProductsResponse},
    description="Get all products in a store by store_id",
)
def get_store_products_handler(path: StorePath):
    with ctx.engine.connect() as conn:
        rows = get_store_products(conn, path.store_id)
        products = map(StoreProduct.from_row, rows)
        response = GetStoreProductsResponse(list(products))
        return response.to_dict(), HTTPStatus.OK


@app.post(
    "/stores/<uuid:store_id>/products",
    responses={201: StoreProduct},
    description="Create a product in a store",
)
def post_store_product_handler(path: StorePath, body: CreateProductDTO):
    with ctx.engine.connect() as conn:
        store = get_store(conn, path.store_id)
        if store is None:
            raise NotFoundException(f"Store {path.store_id} not found")

        row = create_store_product(conn, path.store_id, body)
        product = StoreProduct.from_row(row)
        return product.model_dump(), HTTPStatus.CREATED


@app.delete(
    "/stores/<uuid:store_id>/products/<uuid:product_id>",
    description="Delete a product in a store",
)
def delete_store_product_handler(path: StoreProductPath):
    with ctx.engine.connect() as conn:
        delete_store_product(conn, path.store_id, path.product_id)
        return {}, HTTPStatus.NO_CONTENT


@app.errorhandler(Exception)
def bad_request_handler(e):
    return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@app.errorhandler(NotFoundException)
def not_found_handler(e):
    return {"error": str(e)}, HTTPStatus.NOT_FOUND
