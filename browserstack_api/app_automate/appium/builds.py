import requests

from browserstack_api import Settings
from browserstack_api.app_automate.appium.apps import UploadedApp
from browserstack_api.app_automate.appium.reponses import DeleteResponse
from browserstack_api.app_automate.appium.sessions import Session


class Build:
    def __init__(self, build_id=None, name=None, duration=None, status=None, tags=None,
                 group_id=None, user_id=None, automation_project_id=None, created_at=None,
                 updated_at=None, hashed_id=None, delta=None, test_data=None,
                 sub_group_id=None):
        self.build_id = build_id
        self.name = name
        self.duration = duration
        self.status = status
        self.tags = tags
        self.group_id = group_id
        self.user_id = user_id
        self.automation_project_id = automation_project_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.hashed_id = hashed_id
        self.delta = delta
        self.test_data = test_data
        self.sub_group_id = sub_group_id


class BuildsApi:

    @staticmethod
    def recent_builds(limit=None, offset=None, status=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        url = f"{Settings.base_url}/app-automate/builds.json"

        response = requests.get(url, params=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            builds = [
                Build(**b["automation_build"])
                for b
                in rj
            ]
            return builds
        else:
            raise Exception(f"Invalid Status Code: {response.status_code}")

    @staticmethod
    def details(build_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions.json"
        response = requests.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            sessions = [
                Session(
                    name=s["name"],
                    duration=s["duration"],
                    os=s["os"],
                    os_version=s["os_version"],
                    browser_version=s["browser_version"],
                    browser=s["browser"],
                    device=s["device"],
                    status=s["status"],
                    hashed_id=s["hashed_id"],
                    reason=s["reason"],
                    build_name=s["build_name"],
                    project_name=s["project_name"],
                    logs=s["logs"],
                    browser_url=s["browser_url"],
                    public_url=s["public_url"],
                    appium_logs_url=s["appium_logs_url"],
                    video_url=s["video_url"],
                    app_details=UploadedApp(
                        app_url=s["app_details"]["app_url"],
                        app_name=s["app_details"]["app_name"],
                        app_version=s["app_details"]["app_version"],
                        custom_id=s["app_details"]["app_custom_id"],
                        uploaded_at=s["app_details"]["uploaded_at"]
                    )
                )
                for s
                in [f["automation_session"] for f in rj]
            ]
            return sessions
        else:
            raise Exception(f"Invalid Status Code: {response.status_code}")

    @staticmethod
    def delete(build_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}.json"
        response = requests.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse(
                status=rj["status"],
                message=rj["message"]
            )
        else:
            raise Exception(f"Invalid Status Code: {response.status_code}")
