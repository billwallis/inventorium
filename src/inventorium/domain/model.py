from __future__ import annotations

from typing import Any, Protocol, Self


class DatabaseConnection(Protocol):
    def commit(self) -> None:
        pass  # pragma: no cover

    def rollback(self) -> None:
        pass  # pragma: no cover

    def cursor(self) -> DatabaseCursor:
        pass  # pragma: no cover

    def execute(self, *args: Any, **kwargs: Any) -> DatabaseCursor:
        pass  # pragma: no cover


class DatabaseCursor(Protocol):
    def execute(self, *args: Any, **kwargs: Any) -> Self:
        pass  # pragma: no cover

    def fetchone(self, *args: Any, **kwargs: Any) -> list[Any]:
        pass  # pragma: no cover

    def fetchall(self, *args: Any, **kwargs: Any) -> list[Any]:
        pass  # pragma: no cover
