from bsapi import Settings, Api
from bsapi.models import DeleteResponse


class AutomateSession:
    def __init__(self,
                 name=None,
                 duration=None,
                 os=None,
                 os_version=None,
                 browser_version=None,
                 browser=None,
                 device=None,
                 status=None,
                 hashed_id=None,
                 reason=None,
                 build_name=None,
                 project_name=None,
                 test_priority=None,
                 logs=None,
                 browserstack_status=None,
                 created_at=None,
                 browser_url=None,
                 public_url=None,
                 appium_logs_url=None,
                 video_url=None,
                 browser_console_logs_url=None,
                 har_logs_url=None,
                 selenium_logs_url=None):
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
        self.test_priority = test_priority
        self.logs = logs
        self.browserstack_status = browserstack_status
        self.created_at = created_at
        self.browser_url = browser_url
        self.public_url = public_url
        self.appium_logs_url = appium_logs_url
        self.video_url = video_url
        self.browser_console_logs_url = browser_console_logs_url
        self.har_logs_url = har_logs_url
        self.selenium_logs_url = selenium_logs_url

    @staticmethod
    def by_id(session_id):
        return SessionsApi.details(session_id)

    @staticmethod
    def from_dict(session):
        return AutomateSession(
            name=session["name"] if "name" in session else None,
            duration=session["duration"] if "duration" in session else None,
            os=session["os"] if "os" in session else None,
            os_version=session["os_version"] if "os_version" in session else None,
            browser_version=session["browser_version"] if "browser_version" in session else None,
            browser=session["browser"] if "browser" in session else None,
            device=session["device"] if "device" in session else None,
            status=session["status"] if "status" in session else None,
            hashed_id=session["hashed_id"] if "hashed_id" in session else None,
            reason=session["reason"] if "reason" in session else None,
            build_name=session["build_name"] if "build_name" in session else None,
            project_name=session["project_name"] if "project_name" in session else None,
            test_priority=session["test_priority"] if "test_priority" in session else None,
            logs=session["logs"] if "logs" in session else None,
            browserstack_status=session["browserstack_status"] if "browserstack_status" in session else None,
            created_at=session["created_at"] if "created_at" in session else None,
            browser_url=session["browser_url"] if "browser_url" in session else None,
            public_url=session["public_url"] if "public_url" in session else None,
            appium_logs_url=session["appium_logs_url"] if "appium_logs_url" in session else None,
            video_url=session["video_url"] if "video_url" in session else None,
            browser_console_logs_url=session["browser_console_logs_url"] if "browser_console_logs_url" in session else None,
            har_logs_url=session["har_logs_url"] if "har_logs_url" in session else None,
            selenium_logs_url=session["selenium_logs_url"] if "selenium_logs_url" in session else None
        )

    @staticmethod
    def save_logs(url, file_name):
        with open(file_name, "wb") as f:
            with SessionsApi.get_logs(url) as response:
                f.write(response.content)

    def get_session_logs(self):
        return SessionsApi.get_logs(self.logs)

    def save_session_logs(self, file_name):
        self.save_logs(self.logs, file_name)

    def get_appium_logs(self):
        return SessionsApi.get_logs(self.appium_logs_url)

    def save_appium_logs(self, file_name):
        self.save_logs(self.appium_logs_url, file_name)

    def get_browser_console_logs(self):
        return SessionsApi.get_logs(self.browser_console_logs_url)

    def save_browser_console_logs(self, file_name):
        self.save_logs(self.browser_console_logs_url, file_name)

    def get_har_logs(self):
        return SessionsApi.get_logs(self.har_logs_url)

    def save_har_logs(self, file_name):
        self.save_logs(self.har_logs_url, file_name)

    def get_selenium_logs(self):
        return SessionsApi.get_logs(self.selenium_logs_url)

    def save_selenium_logs(self, file_name):
        self.save_logs(self.selenium_logs_url, file_name)

    def get_video(self):
        return SessionsApi.get_logs(self.video_url)

    def save_video(self, file_name):
        self.save_logs(self.video_url, file_name)

    def update_status(self, status, reason=None):
        session = SessionsApi.update_status(self.hashed_id, status, reason)
        self.status = session.status
        self.reason = session.reason

    def update_name(self, name):
        session = SessionsApi.update_name(self.hashed_id, name)
        self.name = session.name

    def delete(self):
        delete_message = SessionsApi.delete(self.hashed_id)
        return delete_message


class SessionsApi(Api):

    @classmethod
    def details(cls, session_id=None):
        if session_id is None:
            raise ValueError("Session ID is required")

        url = f"{Settings.base_url}/automate/sessions/{session_id}.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]
            return AutomateSession.from_dict(rj)
        else:
            response.raise_for_status()

    @classmethod
    def update_status(cls, session_id, status, reason=None):
        url = f"{Settings.base_url}/automate/sessions/{session_id}.json"

        data = {"status": status}
        if reason is not None:
            data["reason"] = reason

        response = cls.http.put(url, json=data, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]
            return AutomateSession.from_dict(rj)
        else:
            response.raise_for_status()

    @classmethod
    def update_name(cls, session_id, name):
        url = f"{Settings.base_url}/automate/sessions/{session_id}.json"
        data = {"name": name}
        response = cls.http.put(url, json=data, **Settings.request())

        if response.status_code == 200:
            rj = response.json()["automation_session"]
            return AutomateSession.from_dict(rj)
        else:
            response.raise_for_status()

    @classmethod
    def delete(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}.json"
        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            return DeleteResponse.from_dict(response.json())
        else:
            response.raise_for_status()

    @classmethod
    def delete_multiple(cls, session_ids):
        if len(session_ids) < 1:
            raise ValueError()

        query_string = "&".join([f"sessionId={session_id}" for session_id in session_ids])
        url = f"{Settings.base_url}/automate/sessions?{query_string}"

        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            return response.json()["message"]
        else:
            response.raise_for_status()

    @classmethod
    def get_logs(cls, url):
        response = Api.http.get(url, stream=True, **Settings.request())
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    @classmethod
    def get_session_logs(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}/logs"
        return cls.get_logs(url)

    @classmethod
    def get_network_logs(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}/networklogs"
        return cls.get_logs(url)

    @classmethod
    def get_console_logs(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}/consolelogs"
        return cls.get_logs(url)

    @classmethod
    def get_selenium_logs(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}/seleniumlogs"
        return cls.get_logs(url)

    @classmethod
    def get_appium_logs(cls, session_id):
        url = f"{Settings.base_url}/automate/sessions/{session_id}/appiumlogs"
        return cls.get_logs(url)
