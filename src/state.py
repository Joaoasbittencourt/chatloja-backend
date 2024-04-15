import os
from logging import Logger
from dotenv import load_dotenv
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from sqlalchemy import create_engine, Engine


class AppState:
    logger: Logger
    app: OpenAPI
    db: Engine

    def __init__(self):
        load_dotenv()
        DB_CONNECTION = os.getenv("DB_CONNECTION")
        api_info = Info(title="Chatloja API", version="1.0.0")

        self.app = OpenAPI(__name__, info=api_info)
        self.engine = create_engine(DB_CONNECTION)
        self.logger = self.app.logger

        CORS(self.app, resources={r"/*": {"origins": "*"}})
