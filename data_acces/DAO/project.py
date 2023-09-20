from __future__ import annotations

from typing import TYPE_CHECKING

from data_acces.DTO import ProjectInfoDTO

from .base import BaseDAO

if TYPE_CHECKING:
    from data_acces.DTO import ProjectDTO


class ProjectDAO(BaseDAO):
    def create(self, project: ProjectDTO) -> None:
        self._db_gateway.cursor.execute(
            "INSERT INTO projects(name) VALUES(?);", (project.name,)
        )
        self._db_gateway.connection.commit()

    def get_project_id_by_name(self, name: str) -> int:
        project_id = self._db_gateway.cursor.execute(
            "SELECT id FROM projects WHERE name = (?);", (name,)
        ).fetchone()[0]
        return project_id

    def get_all_projects(self) -> list[ProjectInfoDTO]:
        projects = self._db_gateway.cursor.execute("SELECT * FROM projects;").fetchall()
        projects = [
            ProjectInfoDTO(
                project_id=project[0],
                name=project[1],
                created_at=project[2],
                contracts=self._db_gateway.cursor.execute(
                    "SELECT c.id, c.name, s.name FROM contracts c "
                    "JOIN statuses s ON s.id = c.status_id "
                    "WHERE project_id = (?);",
                    (project[0],),
                ).fetchall(),
            )
            for project in projects
        ]
        return projects
