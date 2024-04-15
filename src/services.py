from sqlalchemy import insert, select, Connection

from src.db import stores_table, products_table, stores_products_table
from src.dto import CreateProductDTO


def get_stores(conn: Connection):
    query = select(stores_table)
    rows = conn.execute(query).all()
    return map(lambda row: row._asdict(), rows)


def get_store(conn: Connection, store_id: str):
    query = select(stores_table).where(stores_table.c.id == store_id).limit(1)
    row = conn.execute(query).first()
    store = row._asdict() if row else None
    return store


def get_store_products(conn: Connection, store_id: str):
    query = (
        select(
            products_table.c.id,
            products_table.c.name,
            products_table.c.price,
            products_table.c.image_url,
            stores_products_table.c.category,
            products_table.c.description,
        )
        .select_from(stores_products_table)
        .where(stores_products_table.c.store_id == store_id)
        .join(products_table, stores_products_table.c.product_id == products_table.c.id)
        .order_by(stores_products_table.c.position)
    )
    rows = conn.execute(query).all()
    return map(lambda row: row._asdict(), rows)


def create_store_product(conn: Connection, store_id: str, data: CreateProductDTO):
    pt = products_table
    spt = stores_products_table
    try:
        products = get_store_products(conn, store_id)
        next_position = len(list(products)) + 1
        product_rows = conn.execute(
            (
                insert(pt)
                .values(
                    name=data.name,
                    price=data.price,
                    description=data.description,
                )
                .returning(pt)
            )
        )
        product = product_rows.first()._asdict()
        category = conn.execute(
            (
                insert(spt)
                .values(
                    store_id=store_id,
                    product_id=product["id"],
                    category=data.category,
                    position=next_position,
                )
                .returning(spt.c.category)
            )
        ).scalar_one()
        conn.commit()
        product["category"] = category
        return product

    except Exception as e:
        conn.rollback()
        raise e


def delete_store_product(conn: Connection, store_id: str, product_id: str):
    spt = stores_products_table
    pt = products_table

    try:
        conn.execute(
            spt.delete()
            .filter(spt.c.product_id == product_id)
            .filter(spt.c.store_id == store_id)
        )
        conn.execute(pt.delete().where(pt.c.id == product_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
