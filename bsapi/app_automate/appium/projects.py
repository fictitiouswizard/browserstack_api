from bsapi import Settings, Api
from .builds import Build
from .responses import DeleteResponse


class Project:
    """
    BrowserStack Project

    :param str project_id:
    :param str name:
    :param str group_id:
    :param str user_id:
    :param str created_at:
    :param str updated_at:
    :param str sub_group_id:
    :param builds:
    :type builds: list[:class:`bsapi.app_automate.appium.builds.Build`]
    """
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


class ProjectsApi(Api):

    @classmethod
    def recent_projects(cls, limit=None, offset=None, status=None):
        """
        Get recent projects from BrowserStack

        Example::

            projects = ProjectsApi.recent_projects(limit=20)
            for project in projects:
                print(project.name)

        :param int limit: Number of items to return
        :param int offset: Number of items to skip
        :param str status: Return only items in this status
        :return: List of recent projects
        :rtype: list[:class:`Project`]
        """
        url = f"{Settings.base_url}/app-automate/projects.json"

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status

        response = cls.http.get(url, params=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            projects = [
                Project(
                    project_id=p["id"] if "id" in p else None,
                    name=p["name"] if "name" in p else None,
                    group_id=p["group_id"] if "group_id" in p else None,
                    user_id=p["user_id"] if "user_id" in p else None,
                    created_at=p["created_at"] if "created_at" in p else None,
                    updated_at=p["updated_at"] if "updated_at" in p else None,
                    sub_group_id=p["sub_group_id"] if "sub_group_id" in p else None
                )
                for p
                in rj
            ]
            return projects
        else:
            response.raise_for_status()

    @classmethod
    def details(cls, project_id=None):
        """
        Get the details for a project including recent builds

        Example::

            projects = ProjectsApi.get_recent()
            for project in projects:
                project = ProjectsApi.details(project.project_id)
                for build in project.builds:
                    print(f"{project.name} - {build.name}: {build.status}")


        :param project_id: Project ID
        :return: Project including recent builds
        :rtype: :class:`Project`
        """
        if project_id is None:
            raise ValueError("Project ID cannot be None")

        url = f"{Settings.base_url}/app-automate/projects/{project_id}.json"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["project"]
            return Project(
                project_id=rj["id"] if "id" in rj else None,
                name=rj["name"] if "name" in rj else None,
                group_id=rj["group_id"] if "group_id" in rj else None,
                user_id=rj["user_id"] if "user_id" in rj else None,
                created_at=rj["created_at"] if "created_at" in rj else None,
                updated_at=rj["updated_at"] if "updated_at" in rj else None,
                sub_group_id=rj["sub_group_id"] if "sub_group_id" in rj else None,
                builds=[
                    Build(
                        build_id=b["id"] if "id" in b else None,
                        name=b["name"] if "name" in b else None,
                        duration=b["duration"] if "duration" in b else None,
                        status=b["status"] if "status" in b else None,
                        tags=b["tags"] if "tags" in b else None,
                        group_id=b["group_id"] if "group_id" in b else None,
                        user_id=b["user_id"] if "user_id" in b else None,
                        automation_project_id=b["automation_project_id"] if "automation_project_id" in b else None,
                        created_at=b["created_at"] if "created_at" in b else None,
                        updated_at=b["updated_at"] if "updated_at" in b else None,
                        hashed_id=b["hashed_id"] if "hashed_id" in b else None,
                        delta=b["delta"] if "delta" in b else None,
                        test_data=b["test_data"] if "test_data" in b else None,
                        sub_group_id=b["sub_group_id"] if "sub_group_id" in b else None
                    )
                    for b
                    in rj["builds"]
                ]
            )
        else:
            response.raise_for_status()

    @classmethod
    def update_project_name(cls, project_id=None, name=None):
        """
        Update the name of the project on BrowserStack

        Example::

            projects = ProjectsApi.recent_projects()
            project = [p for p in projects if p.name = "My Test Project"][0]
            updated_project = ProjectsApi.update_project_name(project.project_id, "New Test Project Name")

        :param project_id: Project ID
        :param name: New name for the project
        :return: updated project
        :rtype: :class:`Project`
        """
        if project_id is None:
            raise ValueError("Project ID is required")
        if name is None:
            raise ValueError("Name is required")

        url = f"{Settings.base_url}/app-automate/projects/{project_id}.json"
        data = {"name": name}
        response = cls.http.put(url, json=data, **Settings.request())

        if response.status_code == 200:
            p = response.json()
            project = Project(
                    project_id=p["id"] if "id" in p else None,
                    name=p["name"] if "name" in p else None,
                    group_id=p["group_id"] if "group_id" in p else None,
                    user_id=p["user_id"] if "user_id" in p else None,
                    created_at=p["created_at"] if "created_at" in p else None,
                    updated_at=p["updated_at"] if "updated_at" in p else None,
                    sub_group_id=p["sub_group_id"] if "sub_group_id" in p else None
                )
            return project
        else:
            response.raise_for_status()

    @classmethod
    def status_badge_key(cls, project_id=None):
        """
        Get the status badge for the project

        Example::

            projects = ProjectsApi.recent_projects()
            project = [p for p in projects if p.name == "My Project"][0]
            badge_key = ProjectsApi.get_badge_key(project.project_id)
            badge_markdown = f"[![BrowserStack Status](https://app-automate.browserstack.com/badge.svg?badge_key=<badge_key>)](https://app-automate.browserstack.com/public-build/{badge_key}?redirect=true)"

        :param project_id: Project ID
        :return: Status Badge Key
        :rtype: str
        """
        if project_id is None:
            raise ValueError("Project ID is required")

        url = f"{Settings.base_url}/app-automate/projects/{project_id}/badge_key"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    @classmethod
    def delete(cls, project_id=None):
        """
        Delete the project from BrowserStack.  **You must remove all builds from the project first.**

        Example::

            project = ProjectsApi.details(project_id)
            for build in project.builds:
                message = BuildsApi.delete(build.hashed_id)
                if message.status == "ok":
                    print(f"Deleted: {build.name}")
                else:
                    print(f"{build.name} - {message.message}"
            message = ProjectsApi.delete(project_id)
            if message.status == "ok":
                print(f"{project.name} has been deleted")
            else:
                print(f"{project.name} - {message.message}"

        :param project_id: Project ID to be deleted
        :return: Deleted response message
        :rtype: :class:`.responses.DeleteResponse`
        """
        if project_id is None:
            raise ValueError("Project ID is required")

        url = f"{Settings.base_url}/app-automate/projects/{project_id}.json"
        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse(
                status=rj["status"],
                message=rj["message"]
            )
        else:
            response.raise_for_status()
