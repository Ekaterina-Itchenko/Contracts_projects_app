from __future__ import annotations

from typing import TYPE_CHECKING

from data_acces.DAO import ContractDAO
from data_acces.DTO import ContractDTO

from .errors import (ActiveContractsAlreadyExistError,
                     ContractDoesNotExistError,
                     ContractHasUsedWithAtherProjectError,
                     InvalidContractStatusError)

if TYPE_CHECKING:
    from data_acces.DTO import ContractInfoDTO
    from interfaces import DBGatewayProtocol


class ContractService:
    def __init__(self, db_connector: DBGatewayProtocol) -> None:
        self._dao = ContractDAO(db_gateway=db_connector)

    def create_contract(self, name: str):
        contract_data = ContractDTO(name=name)
        self._dao.create(contract=contract_data)

    def add_project(self, contract_id: int, project_id: int) -> None:
        if contract_id in self._dao.get_id_list():
            contract = self._dao.get_contract(contract_id=contract_id)
            if contract.project_id:
                raise ContractHasUsedWithAtherProjectError(
                    "The contract has used with another project'."
                )
            if contract.status != "active":
                raise InvalidContractStatusError(
                    "The contract status must be 'active'."
                )
            for contract in self._dao.get_contracts_by_project_id(
                project_id=project_id
            ):
                if contract.status == "active":
                    raise ActiveContractsAlreadyExistError(
                        "This project has active contracts."
                    )
            self._dao.add_project(project_id=project_id, contract_id=contract_id)
        else:
            raise ContractDoesNotExistError("Contract does not exist.")

    def complete_contract(self, contract_id: int) -> None:
        self._dao.complete_contract(contract_id=contract_id)

    def confirm_contract(self, contract_id: int) -> None:
        self._dao.confirm_contract(contract_id=contract_id)

    def get_contracts_list(self) -> list[ContractInfoDTO]:
        contracts_list = self._dao.get_all_contracts()
        return contracts_list
