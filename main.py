import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.errors import NotFoundException
from src.product_service import ProductService
from src.store_service import StoreService

load_dotenv()
DB_CONNECTION = os.getenv("DB_CONNECTION")
app = Flask(__name__)

logger = app.logger
engine = create_engine(DB_CONNECTION)
session = Session(engine)
product_service = ProductService(session)
store_service = StoreService(session)

engine.connect()
CORS(app, resources={r"/*": {"origins": "*"}})


@app.get("/stores/<uuid:store_id>")
def fetch_store(store_id):
    store = store_service.get_store(store_id)

    if store is None:
        return {"error": "Store not found"}, 404
    return store.to_dict()


@app.get("/stores")
def list_stores():
    rows = store_service.get_stores()
    stores = map(lambda row: row.to_dict(), rows)
    return list(stores)


@app.get("/stores/<uuid:store_id>/products")
def list_store_products(store_id):
    rows = product_service.get_store_products(store_id)
    return list(rows)


@app.errorhandler(Exception)
def handle_bad_request(e):
    return {"error": str(e)}, 400


@app.errorhandler(NotFoundException)
def handle_not_found(e):
    return {"error": str(e)}, 404
