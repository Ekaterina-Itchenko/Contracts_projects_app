from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ContractDTO:
    name: str
    status_id: int = 1
    signed_at: Optional[datetime] = None
    project_id: Optional[int] = None


@dataclass
class ContractInfoDTO:
    contract_id: int
    name: str
    status: str
    signed_at: Optional[datetime]
    project_id: int
    project_name: Optional[str]
    created_at: datetime
