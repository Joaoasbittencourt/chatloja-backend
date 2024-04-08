from src.db import Store
from sqlalchemy import select
from sqlalchemy.orm import Session


class StoreService:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_stores(self):
        return self.session.scalars(select(Store)).all()

    def get_store(self, store_id: str):
        return self.session.get(Store, store_id)
