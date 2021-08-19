from bsapi import Settings, Api
from bsapi.app_automate.appium.responses import DeleteResponse
from bsapi.app_automate.appium.apps import UploadedApp


class SessionStatus:
    passed = "passed"
    failed = "failed"


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


class SessionsApi(Api):

    @classmethod
    def details(cls, session_id=None):
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]

            return Session(
                name=rj["name"] if "name" in rj else None,
                duration=rj["duration"] if "duration" in rj else None,
                os=rj["os"] if "os" in rj else None,
                os_version=rj["os_version"] if "os_version" in rj else None,
                browser_version=rj["browser_version"] if "browser_version" in rj else None,
                browser=rj["browser"] if "browser" in rj else None,
                device=rj["device"] if "device" in rj else None,
                status=rj["status"] if "status" in rj else None,
                hashed_id=rj["hashed_id"] if "hashed_id" in rj else None,
                reason=rj["reason"] if "reason" in rj else None,
                build_name=rj["build_name"] if "build_name" in rj else None,
                project_name=rj["project_name"] if "project_name" in rj else None,
                logs=rj["logs"] if "logs" in rj else None,
                browser_url=rj["browser_url"] if "browser_url" in rj else None,
                public_url=rj["public_url"] if "public_url" in rj else None,
                appium_logs_url=rj["appium_logs_url"] if "appium_logs_url" in rj else None,
                video_url=rj["video_url"] if "video_url" in rj else None,
                device_logs_url=rj["device_logs_url"] if "device_logs_url" in rj else None,
                app_details=UploadedApp(
                    app_url=rj["app_details"]["app_url"] if "app_url" in rj["app_details"] else None,
                    app_name=rj["app_details"]["app_name"] if "app_name" in rj["app_details"] else None,
                    app_version=rj["app_details"]["app_version"] if "app_version" in rj["app_details"] else None,
                    custom_id=rj["app_details"]["app_custom_id"] if "app_custom_id" in rj["app_details"] else None,
                    uploaded_at=rj["app_details"]["uploaded_at"] if "uploaded_at" in rj["app_details"] else None
                )
            )
        else:
            response.raise_for_status()

    @classmethod
    def update_status(cls, session_id=None, status=None, reason=None):
        if session_id is None:
            raise ValueError("Session ID is required")
        if status is None:
            raise ValueError("Status is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        data = {"status": status}
        if reason is not None:
            data["reason"] = reason

        response = cls.http.put(url, json=data, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]
            return Session(
                name=rj["name"] if "name" in rj else None,
                duration=rj["duration"] if "duration" in rj else None,
                os=rj["os"] if "os" in rj else None,
                os_version=rj["os_version"] if "os_version" in rj else None,
                browser_version=rj["browser_version"] if "browser_version" in rj else None,
                browser=rj["browser"] if "browser" in rj else None,
                device=rj["device"] if "device" in rj else None,
                status=rj["status"] if "status" in rj else None,
                hashed_id=rj["hashed_id"] if "hashed_id" in rj else None,
                reason=rj["reason"] if "reason" in rj else None,
                build_name=rj["build_name"] if "build_name" in rj else None,
                project_name=rj["project_name"] if "project_name" in rj else None
            )
        else:
            response.raise_for_status()

    @classmethod
    def delete(cls, session_id=None):
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/sessions/{session_id}.json"

        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return DeleteResponse(
                status=rj["status"],
                message=rj["message"]
            )
        else:
            response.raise_for_status()

    @classmethod
    def get_text_logs(cls, build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/logs"
        response = cls.http.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @classmethod
    def get_device_logs(cls, build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/devicelogs"
        response = cls.http.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @classmethod
    def get_appium_logs(cls, build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/appiumlogs"

        response = cls.http.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @classmethod
    def get_network_logs(cls, build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/networklogs"

        response = cls.http.get(url, stream=True, **Settings.request())

        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @classmethod
    def get_profiling_data(cls, build_id=None, session_id=None):
        if build_id is None:
            raise ValueError("Build ID is required")
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/app-automate/builds/{build_id}/sessions/{session_id}/appprofiling"

        response = cls.http.get(url, **Settings.request())

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










