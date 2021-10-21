from bsapi import Settings, Api
from bsapi.models import DeleteResponse, Project, Build


class AutomateProject(Project):

    @staticmethod
    def by_id(project_id):
        return ProjectsApi.details(project_id)

    def update_name(self, name):
        project = ProjectsApi.update_name(self.project_id, name)
        self.name = project.name

    def get_status_badge(self):
        status_badge = ProjectsApi.get_status_badge(self.project_id)
        return status_badge

    def delete(self):
        delete_response = ProjectsApi.delete_project(self.project_id)
        return delete_response


class ProjectsApi(Api):

    @classmethod
    def get_project_list(cls):
        url = f"{Settings.base_url}/automate/projects.json"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [AutomateProject.from_dict(p) for p in rj]
        else:
            response.raise_for_status()

    @classmethod
    def details(cls, project_id):
        url = f"{Settings.base_url}/automate/projects/{project_id}.json"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            project = AutomateProject.from_dict(rj["project"])
            project.builds = [Build.from_dict(build) for build in rj["project"]["builds"]]
            return project
        else:
            response.raise_for_status()

    @classmethod
    def get_status_badge(cls, project_id):
        url = f"{Settings.base_url}/automate/projects/{project_id}/badge_key"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rt = response.text
            return rt
        else:
            response.raise_for_status()

    @classmethod
    def update_name(cls, project_id, name):
        url = f"{Settings.base_url}/automate/projects/{project_id}.json"
        response = cls.http.put(url, json={"name": name}, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return Project.from_dict(rj)
        else:
            response.raise_for_status()

    @classmethod
    def delete_project(cls, project_id):
        url = f"{Settings.base_url}/automate/projects/{project_id}.json"
        response = cls.http.delete(url, project_id)

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse.from_dict(rj)
        else:
            response.raise_for_status()