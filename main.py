from http import HTTPStatus
from src.dto import CreateProductDTO, StorePath, StoreProductPath
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


@app.get("/stores/<uuid:store_id>")
def get_store_handler(path: StorePath):
    with ctx.engine.connect() as conn:
        store = get_store(conn, path.store_id)
        if store is None:
            raise NotFoundException(f"Store {path.store_id} not found")
        return store, HTTPStatus.OK


@app.get("/stores")
def get_stores_handler():
    with ctx.engine.connect() as conn:
        rows = get_stores(conn)
        return list(rows), HTTPStatus.OK


@app.get("/stores/<uuid:store_id>/products")
def get_store_products_handler(path: StorePath):
    with ctx.engine.connect() as conn:
        rows = get_store_products(conn, path.store_id)
        return list(rows), HTTPStatus.OK


@app.post("/stores/<uuid:store_id>/products")
def post_store_product_handler(path: StorePath, body: CreateProductDTO):
    with ctx.engine.connect() as conn:
        store = get_store(conn, path.store_id)
        if store is None:
            raise NotFoundException(f"Store {path.store_id} not found")

        product = create_store_product(conn, path.store_id, body)
        return product, HTTPStatus.CREATED


@app.delete("/stores/<uuid:store_id>/products/<uuid:product_id>")
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
