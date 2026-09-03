from __future__ import annotations

import dataclasses
from typing import Any

from inventorium.domain.model import DatabaseConnection, cursor_ctx


@dataclasses.dataclass
class InventoryCreationData:
    store_id: int
    product_id: int
    in_stock: int = dataclasses.field(default=0)


@dataclasses.dataclass
class InventoryResource:
    store_id: int
    product_id: int
    in_stock: int

    def __str__(self) -> str:
        return f"Store {self.store_id}, Product ({self.product_id}) (In stock: {self.in_stock})"

    @classmethod
    def from_result_set(cls, result_set: list[Any]) -> InventoryResource:
        if result_set:
            return InventoryResource(
                store_id=result_set[0],
                product_id=result_set[1],
                in_stock=result_set[2],
            )
        raise IndexError("Inventory not found")


class InventoryStore:
    def __init__(self, db_conn: DatabaseConnection) -> None:
        self.db_conn = db_conn

    def create(self, data: InventoryCreationData) -> InventoryResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                insert into inventory (store_id, product_id, in_stock)
                values (:store_id, :product_id, :in_stock)
                returning store_id, product_id, in_stock
                """,
                {
                    "store_id": data.store_id,
                    "product_id": data.product_id,
                    "in_stock": data.in_stock,
                },
            )
            result = InventoryResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def read(self, store_id: int, product_id: int) -> InventoryResource:
        result = self.db_conn.execute(
            """
            select store_id, product_id, in_stock
            from inventory
            where store_id = :store_id
              and product_id = :product_id
              and not deleted
            """,
            {
                "store_id": store_id,
                "product_id": product_id,
            },
        )
        return InventoryResource.from_result_set(result.fetchone())

    def update(self, resource: InventoryResource) -> InventoryResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update inventory
                set in_stock = :in_stock
                where store_id = :store_id
                  and product_id = :product_id
                returning store_id, product_id, in_stock
                """,
                {
                    "store_id": resource.store_id,
                    "product_id": resource.product_id,
                    "in_stock": resource.in_stock,
                },
            )
            result = InventoryResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def delete(self, store_id: int, product_id: int) -> InventoryResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update inventory
                set deleted = true
                where store_id = :store_id
                  and product_id = :product_id
                returning store_id, product_id, in_stock
                """,
                {
                    "store_id": store_id,
                    "product_id": product_id,
                },
            )
            result = InventoryResource(*cursor.fetchone())

        self.db_conn.commit()
        return result
