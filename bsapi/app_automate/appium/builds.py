from bsapi import Settings, Api
from .apps import UploadedApp
from .responses import DeleteResponse


class Build:
    """
    :var str build_id: Unique ID for the build
    :var str name: Build name
    :var str duration:
    :var str status:
    :var str tags:
    :var str group_id:
    :var str user_id:
    :var automation_project_id:
    :var str created_at:
    :var str updated_at:
    :var str hashed_id:
    :var str delta:
    :var str test_data:
    :var str sub_group_id:
    """
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


class BuildsApi(Api):
    """
    Class for interacting with the Builds REST endpoint
    """

    @classmethod
    def recent_builds(cls, limit=None, offset=None, status=None):
        """
        Fetch Recent builds from BrowserStack

        Example::

            builds = BuildsApi.recent_builds(limit=5)

        :param int limit:
        :param int offset:
        :param int status:
        :return: Returns a list of Builds
        :rtype: list[:class:`bsapi.app_automate.appium.builds.Build`]
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        url = f"{Settings.base_url}/app-automate/builds.json"

        response = cls.http.get(url, params=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            builds = [
                Build(**b["automation_build"])
                for b
                in rj
            ]
            return builds
        else:
            response.raise_for_status()

    @classmethod
    def details(cls, build_id=None):
        """
        Retrieve recent sessions for a build

        Example::

            builds = BuildsApi.recent_builds(limit=5)
            for build in builds:
                sessions = BuildsApi.details(build.hashed_id)
                for session in sessions:
                    print(f"{session.name} - {session.status}"

        :param str build_id:
        :return: A list of Sessions
        :rtype: list[:class:`bsapi.app_automate.appium.sessions.Session`]
        """
        if build_id is None:
            raise ValueError("Build ID is required")

        from .sessions import Session

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions.json"
        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            sessions = [
                Session(
                    name=s["name"] if "name" in s else None,
                    duration=s["duration"] if "duration" in s else None,
                    os=s["os"] if "os" in s else None,
                    os_version=s["os_version"] if "os_version" in s else None,
                    browser_version=s["browser_version"] if "browser_version" in s else None,
                    browser=s["browser"] if "browser" in s else None,
                    device=s["device"] if "device" in s else None,
                    status=s["status"] if "status" in s else None,
                    hashed_id=s["hashed_id"] if "hashed_id" in s else None,
                    reason=s["reason"] if "reason" in s else None,
                    build_name=s["build_name"] if "build_name" in s else None,
                    project_name=s["project_name"] if "project_name" in s else None,
                    logs=s["logs"] if "logs" in s else None,
                    browser_url=s["browser_url"] if "browser_url" in s else None,
                    public_url=s["public_url"] if "public_url" in s else None,
                    appium_logs_url=s["appium_logs_url"] if "appium_logs_url" in s else None,
                    video_url=s["video_url"] if "video_url" in s else None,
                    app_details=UploadedApp(
                        app_url=s["app_details"]["app_url"] if "app_url" in s["app_details"] else None,
                        app_name=s["app_details"]["app_name"] if "app_name" in s["app_details"] else None,
                        app_version=s["app_details"]["app_version"] if "app_version" in s["app_details"] else None,
                        custom_id=s["app_details"]["app_custom_id"] if "app_custom_id" in s["app_details"] else None,
                        uploaded_at=s["app_details"]["uploaded_at"] if "uploaded_at" in s["app_details"] else None
                    )
                )
                for s
                in [f["automation_session"] for f in rj]
            ]
            return sessions
        else:
            response.raise_for_status()

    @classmethod
    def delete(cls, build_id=None):
        """
        Delete a build from BrowserStack.  Removing a build will remove all sessions associated with it.

        Example::

            builds = BuildsApi.recent_builds()
            if len(builds) > 0:
                build = builds[0]
                response = BuildsApi.delete(build.hashed_id)
                if response.status == "ok":
                    print("The build was deleted")

        :param build_id:
        :return:
        """
        if build_id is None:
            raise ValueError("Build ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}.json"
        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse(
                status=rj["status"],
                message=rj["message"]
            )
        else:
            response.raise_for_status()
