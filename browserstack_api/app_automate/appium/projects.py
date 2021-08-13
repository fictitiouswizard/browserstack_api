import requests

from browserstack_api import Settings
from .builds import Build


class Project:
    def __init__(self, project_id=None, name=None, group_id=None, user_id=None,
                 created_at=None, updated_at=None, sub_group_id=None, builds=None):
        self.project_id = project_id
        self.name = name
        self.group_id = group_id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.sub_group_id = sub_group_id
        self.builds = builds


class ProjectsApi:

    recent_projects_path = "/app-automate/projects.json"

    @staticmethod
    def recent_projects(limit=None, offset=None, status=None):
        url = f"{Settings.base_url}{ProjectsApi.recent_projects_path}"

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status

        response = requests.get(url, params=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            projects = [
                Project(
                    project_id=p["project_id"],
                    name=p["name"],
                    group_id=p["group_id"],
                    user_id=p["user_id"],
                    created_at=p["created_at"],
                    updated_at=p["updated_at"],
                    sub_group_id=p["sub_group_id"]
                )
                for p
                in rj
            ]
            return projects
        else:
            raise Exception(f"Invalid Status Code: {response.status_code}")

    @staticmethod
    def details(project_id=None):
        if project_id is None:
            raise ValueError("Project ID cannot be None")

        url = f"{Settings.base_url}/app-automate/projects/{project_id}.json"
        response = requests.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return Project(
                project_id=rj["id"],
                name=rj["name"],
                group_id=rj["group_id"],
                user_id=rj["user_id"],
                created_at=rj["created_at"],
                updated_at=rj["updated_at"],
                sub_group_id=rj["sub_group_id"],
                builds=[
                    Build(
                        build_id=b["id"],
                        name=b["name"],
                        duration=b["duration"],
                        status=b["status"],
                        tags=b["tags"],
                        group_id=b["group_id"],
                        user_id=b["user_id"],
                        automation_project_id=b["automation_project_id"],
                        created_at=b["created_at"],
                        updated_at=b["updated_at"],
                        hashed_id=b["hashed_id"],
                        delta=b["delta"],
                        test_data=b["test_data"],
                        sub_group_id=b["sub_group_id"]
                    )
                    for b
                    in rj["builds"]
                ]
            )
        else:
            raise Exception(f"Invalid Status Code: {response.status_code}")

    @staticmethod
    def update_project_name(project_id=None, name=None):
        # TODO
        # https://www.browserstack.com/docs/app-automate/api-reference/appium/projects#update-project-details
        if project_id is None:
            raise ValueError("Project ID is required")
        if name is None:
            raise ValueError("Name is required")


