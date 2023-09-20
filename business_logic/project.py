from __future__ import annotations

from typing import TYPE_CHECKING

from data_acces.DAO import ContractDAO, ProjectDAO
from data_acces.DTO import ProjectDTO

from .errors import (NoContractsError, ProjectAlreadyExistsError,
                     ProjectDoesNotExistError)

if TYPE_CHECKING:
    from data_acces.DTO import ProjectInfoDTO
    from interfaces import DBGatewayProtocol


class ProjectService:
    def __init__(self, db_connector: DBGatewayProtocol) -> None:
        self._dao = ProjectDAO(db_gateway=db_connector)
        self._contract_dao = ContractDAO(db_gateway=db_connector)

    def create_project(self, name: str) -> None:
        if name in self._get_all_projects_name():
            raise ProjectAlreadyExistsError(
                f"The project '{name}' has already existed."
            )
        if self._contract_dao.get_all_contracts():
            project_data = ProjectDTO(name=name)
            self._dao.create(project=project_data)
        else:
            raise NoContractsError(
                "There are no contracts. You can't create any projects."
            )

    def get_id_by_name(self, name: str) -> int:
        if name in self._get_all_projects_name():
            result = self._dao.get_project_id_by_name(name=name)
            return result
        else:
            raise ProjectDoesNotExistError(f"The project '{name}' does not exist.")

    def get_all_projects(self) -> list[ProjectInfoDTO]:
        projects = self._dao.get_all_projects()
        return projects

    def _get_all_projects_name(self) -> list[str]:
        projects_names = [project.name for project in self._dao.get_all_projects()]
        return projects_names
