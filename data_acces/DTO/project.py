from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class ProjectDTO:
    name: str


@dataclass
class ProjectInfoDTO:
    project_id: int
    name: str
    created_at: datetime
    contracts: list[tuple[int, str, str]]
