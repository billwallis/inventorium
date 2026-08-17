from __future__ import annotations

import dataclasses
from typing import Any

from inventorium.domain.model import DatabaseConnection, cursor_ctx

# TODO: Consider using SQLite adapters:
#       https://docs.python.org/3/library/sqlite3.html#how-to-adapt-custom-python-types-to-sqlite-values


@dataclasses.dataclass
class ProductCreationData:
    name: str


@dataclasses.dataclass
class ProductResource:
    id: int
    name: str

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ProductResource):
            return self.id == other.id
        else:
            return NotImplemented

    @classmethod
    def from_result_set(cls, result_set: list[Any]) -> ProductResource:
        if result_set:
            return ProductResource(
                id=result_set[0],
                name=result_set[1],
            )
        raise IndexError("Product not found")


class ProductStore:
    def __init__(self, db_conn: DatabaseConnection) -> None:
        self.db_conn = db_conn

    def create(self, data: ProductCreationData) -> ProductResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                insert into products (product_name)
                values (:product_name)
                returning product_id, product_name
                """,
                {"product_name": data.name},
            )
            result = ProductResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def read(self, product_id: int) -> ProductResource:
        result = self.db_conn.execute(
            """
            select product_id, product_name
            from products
            where product_id = :id
              and not deleted
            """,
            {"id": product_id},
        )
        return ProductResource.from_result_set(result.fetchone())

    def update(self, resource: ProductResource) -> ProductResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update products
                set product_name = :product_name
                where product_id = :product_id
                returning product_id, product_name
                """,
                {
                    "product_id": resource.id,
                    "product_name": resource.name,
                },
            )
            result = ProductResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def delete(self, product_id: int) -> ProductResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update products
                set deleted = true
                where product_id = :product_id
                returning product_id, product_name
                """,
                {"product_id": product_id},
            )
            result = ProductResource(*cursor.fetchone())

        self.db_conn.commit()
        return result
