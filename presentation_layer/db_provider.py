from __future__ import annotations

from typing import TYPE_CHECKING

from presentation_layer.db_connector import SqliteGateway
from presentation_layer.errors import InvalidDBTypeError

if TYPE_CHECKING:
    from interfaces import DBGatewayProtocol


def db_provider(db_name: str, db_type: str) -> DBGatewayProtocol:
    if db_type == "sqlite":
        return SqliteGateway(db_name=db_name)
    else:
        raise InvalidDBTypeError("Invalid configuration data - type of database.")
