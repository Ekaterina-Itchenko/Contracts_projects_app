from __future__ import annotations

from typing import TYPE_CHECKING

from data_acces.DTO import ContractInfoDTO

from .base import BaseDAO

if TYPE_CHECKING:
    from data_acces.DTO import ContractDTO


class ContractDAO(BaseDAO):
    def create(self, contract: ContractDTO) -> None:
        self._db_gateway.cursor.execute(
            "INSERT INTO contracts(name, status_id, signed_at, project_id) VALUES(?, ?, ?, ?);",
            (
                contract.name,
                contract.status_id,
                contract.signed_at,
                contract.project_id,
            ),
        )
        self._db_gateway.connection.commit()

    def add_project(self, project_id: int, contract_id: int) -> None:
        self._db_gateway.cursor.execute(
            "UPDATE contracts SET project_id = (?) WHERE id = (?);",
            (project_id, contract_id),
        )
        self._db_gateway.connection.commit()

    def get_contract(self, contract_id: int) -> ContractInfoDTO:
        contract = self._db_gateway.cursor.execute(
            "SELECT c.id, c.name, s.name, p.name, c.signed_at, c.created_at, "
            "c.project_id FROM contracts c "
            "JOIN statuses s ON c.status_id = s.id "
            "LEFT JOIN projects p ON p.id = c.project_id "
            "WHERE c.id = (?);",
            (contract_id,),
        ).fetchone()
        contract = ContractInfoDTO(
            contract_id=contract[0],
            name=contract[1],
            status=contract[2],
            signed_at=contract[4],
            project_name=contract[3],
            created_at=contract[5],
            project_id=contract[6],
        )
        return contract

    def get_contracts_by_project_id(self, project_id: int) -> list[ContractInfoDTO]:
        contracts_list = self._db_gateway.cursor.execute(
            "SELECT c.id, c.name, s.name, p.name, c.signed_at, c.created_at, c.project_id FROM contracts c "
            "JOIN statuses s ON c.status_id = s.id "
            "LEFT JOIN projects p ON p.id = c.project_id "
            "WHERE c.project_id = (?);",
            (project_id,),
        ).fetchall()
        contracts = [
            ContractInfoDTO(
                contract_id=contract[0],
                name=contract[1],
                status=contract[2],
                signed_at=contract[4],
                project_name=contract[3],
                created_at=contract[5],
                project_id=contract[6],
            )
            for contract in contracts_list
        ]
        return contracts

    def confirm_contract(self, contract_id: int) -> None:
        self._db_gateway.cursor.execute(
            "UPDATE contracts SET status_id = (?), signed_at = CURRENT_TIMESTAMP WHERE id = (?);",
            (2, contract_id),
        )
        self._db_gateway.connection.commit()

    def complete_contract(self, contract_id: int) -> None:
        self._db_gateway.cursor.execute(
            "UPDATE contracts SET status_id = (?) WHERE id = (?);", (3, contract_id)
        )
        self._db_gateway.connection.commit()

    def get_all_contracts(self) -> list[ContractInfoDTO]:
        contracts = self._db_gateway.cursor.execute(
            "SELECT c.id, c.name, s.name, c.created_at, c.signed_at, p.name, c.project_id FROM contracts c "
            "LEFT LEFT JOIN projects p ON p.id = c.project_id "
            "LEFT JOIN statuses s ON c.status_id = s.id;"
        ).fetchall()
        contracts = [
            ContractInfoDTO(
                contract_id=contract[0],
                name=contract[1],
                status=contract[2],
                signed_at=contract[4],
                project_name=contract[5],
                created_at=contract[3],
                project_id=contract[6],
            )
            for contract in contracts
        ]
        return contracts

    def get_id_list(self) -> list[int]:
        id_list = [contract.contract_id for contract in self.get_all_contracts()]
        return id_list
