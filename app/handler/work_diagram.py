from typing import Optional, List
from app.models.work_diagram import WorkProject
from app.services.WorkDiagram import fetch_work_projects


class WorkDiagramHandler:
    async def fetch_projects(self) -> List[WorkProject]:
        all_projects = await fetch_work_projects()
        return all_projects

    async def fetch_project_by_id(self, project_id: int) -> Optional[WorkProject]:
        all_projects = await fetch_work_projects()

        for project in all_projects:
            if project.id == project_id:
                return project

        return None

    async def fetch_projects_by_agency(self, agency: str) -> List[WorkProject]:
        all_projects = await fetch_work_projects()

        filtered_projects = [
            project for project in all_projects if agency in project.executing_agency
        ]

        return filtered_projects

    async def fetch_projects_by_name(self, keyword: str) -> List[WorkProject]:
        all_projects = await fetch_work_projects()

        filtered_projects = [
            project for project in all_projects if keyword in project.project_name
        ]

        return filtered_projects
