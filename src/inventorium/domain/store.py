from __future__ import annotations

import dataclasses
from typing import Any

from inventorium.domain.model import DatabaseConnection, cursor_ctx


@dataclasses.dataclass
class StoreCreationData:
    name: str


@dataclasses.dataclass
class StoreResource:
    id: int
    name: str

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StoreResource):
            return self.id == other.id
        else:
            return NotImplemented

    @classmethod
    def from_result_set(cls, result_set: list[Any]) -> StoreResource:
        if result_set:
            return StoreResource(
                id=result_set[0],
                name=result_set[1],
            )
        raise IndexError("Store not found")


class StoreStore:
    def __init__(self, db_conn: DatabaseConnection) -> None:
        self.db_conn = db_conn

    def create(self, data: StoreCreationData) -> StoreResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                insert into stores (store_name)
                values (:store_name)
                returning store_id, store_name
                """,
                {"store_name": data.name},
            )
            result = StoreResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def read(self, store_id: int) -> StoreResource:
        result = self.db_conn.execute(
            """
            select store_id, store_name
            from stores
            where store_id = :id
              and not deleted
            """,
            {"id": store_id},
        )
        return StoreResource.from_result_set(result.fetchone())

    def update(self, resource: StoreResource) -> StoreResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update stores
                set store_name = :store_name
                where store_id = :store_id
                returning store_id, store_name
                """,
                {
                    "store_id": resource.id,
                    "store_name": resource.name,
                },
            )
            result = StoreResource(*cursor.fetchone())

        self.db_conn.commit()
        return result

    def delete(self, store_id: int) -> StoreResource:
        with cursor_ctx(self.db_conn) as cursor:
            cursor.execute(
                """
                update stores
                set deleted = true
                where store_id = :store_id
                returning store_id, store_name
                """,
                {"store_id": store_id},
            )
            result = StoreResource(*cursor.fetchone())

        self.db_conn.commit()
        return result
