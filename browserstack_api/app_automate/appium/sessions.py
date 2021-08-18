import requests

from browserstack_api import Settings
from browserstack_api.app_automate.appium.responses import DeleteResponse
from browserstack_api.app_automate.appium.apps import UploadedApp


class Session:
    def __init__(self, name=None, duration=None, os=None, os_version=None,
                 browser_version=None, browser=None, device=None, status=None,
                 hashed_id=None, reason=None, build_name=None, project_name=None,
                 logs=None, browser_url=None, public_url=None, appium_logs_url=None,
                 video_url=None, device_logs_url=None, app_details=None):
        self.name = name
        self.duration = duration
        self.os = os
        self.os_version = os_version
        self.browser_version = browser_version
        self.browser = browser
        self.device = device
        self.status = status
        self.hashed_id = hashed_id
        self.reason = reason
        self.build_name = build_name
        self.project_name = project_name
        self.logs = logs
        self.browser_url = browser_url
        self.public_url = public_url
        self.appium_logs_url = appium_logs_url
        self.video_url = video_url
        self.device_logs_url = device_logs_url
        self.app_details = app_details


class AppProfilingData:
    def __init__(self, ts=None, cpu=None, mem=None, mema=None, batt=None,
                 temp=None):
        self.timestamp = ts
        self.cpu = cpu
        self.memory = mem
        self.memory_available = mema
        self.battery = batt
        self.temperature = temp


class SessionApi:

    @staticmethod
    def details(session_id=None):
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        response = requests.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]

            return Session(
                name=rj["name"],
                duration=rj["duration"],
                os=rj["os"],
                os_version=rj["os_version"],
                browser_version=rj["browser_version"],
                browser=rj["browser"],
                device=rj["device"],
                status=rj["status"],
                hashed_id=rj["hashed_id"],
                reason=rj["reason"],
                build_name=rj["build_name"],
                project_name=rj["project_name"],
                logs=rj["logs"],
                browser_url=rj["browser_url"],
                public_url=rj["public_url"],
                appium_logs_url=rj["appium_logs_url"],
                video_url=rj["video_url"],
                device_logs_url=rj["device_logs_url"],
                app_details=UploadedApp(
                    app_url=rj["app_details"]["app_url"],
                    app_name=rj["app_details"]["app_name"],
                    app_version=rj["app_details"]["app_version"],
                    custom_id=rj["app_details"]["app_custom_id"],
                    uploaded_at=rj["app_details"]["uploaded_at"]
                )
            )
        else:
            response.raise_for_status()

    @staticmethod
    def update_status(session_id=None, status=None, reason=None):
        if session_id is None:
            raise ValueError("Session ID is required")
        if status is None:
            raise ValueError("Status is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        data = {"status": status}
        if reason is not None:
            data["reason"] = reason

        response = requests.put(url, json=data, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]
            return Session(
                name=rj["name"],
                duration=rj["duration"],
                os=rj["os"],
                os_version=["os_version"],
                browser_version=rj["browser_version"],
                browser=rj["browser"],
                device=rj["device"],
                status=rj["status"],
                hashed_id=rj["hashed_id"],
                reason=rj["reason"],
                build_name=rj["build_name"],
                project_name=rj["project_name"]
            )
        else:
            response.raise_for_status()

    @staticmethod
    def delete(session_id=None):
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        response = requests.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse(
                status=rj["status"],
                message=rj["message"]
            )
        else:
            response.raise_for_status()

    @staticmethod
    def get_text_logs(build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/logs"

        response = requests.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @staticmethod
    def get_device_logs(build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/devicelogs"

        response = requests.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @staticmethod
    def get_appium_logs(build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/appiumlogs"

        response = requests.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @staticmethod
    def get_network_logs(build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/networklogs"

        response = requests.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @staticmethod
    def get_profiling_data(build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/appprofiling"

        response = requests.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                AppProfilingData(
                    ts=apd["ts"],
                    cpu=apd["cpu"],
                    mem=apd["mem"],
                    mema=apd["mema"],
                    batt=apd["batt"],
                    temp=apd["temp"]
                )
                for apd
                in rj
            ]
        else:
            response.raise_for_status()










