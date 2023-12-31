from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from sqlite3 import Connection, Cursor


class DBGatewayProtocol(Protocol):
    connection: Connection
    cursor: Cursor


class CreateRecordProtocol(Protocol):
    def create(self, data: object) -> None:
        raise NotImplementedError
