from bsapi import Settings, Api
from .responses import DeleteResponse
from .apps import UploadedApp
from .projects import ProjectsApi
from .builds import BuildsApi


class SessionStatus:
    """
    Represents the Session Status options

    :param str passed: Passed
    :param str failed: Failed
    """
    passed = "passed"
    failed = "failed"


class Session:
    """
    BrowserStack Session

    :param str name:
    :param str duration:
    :param str os:
    :param str os_version:
    :param str browser_version:
    :param str browser:
    :param str device:
    :param str status:
    :param str hashed_id:
    :param str reason:
    :param str build_name:
    :param str project_name:
    :param str logs:
    :param str browser_url:
    :param str public_url:
    :param str appium_logs_url:
    :param str video_url:
    :param str device_logs_url:
    :param app_details:
    :type app_details: :class:`bsapi.app_automate.appium.apps.UploadedApp`
    :param build:
    :type build: :class:`bsapi.app_automate.appium.builds.Build`
    :param project:
    :type project: :class:`bsapi.app_automate.appium.projects.Project`
    """
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
        self._build = None
        self._project = None

    @property
    def build(self):
        if self._build is None:
            offset = 0
            builds = BuildsApi.recent_builds(20, offset)
            filtered_builds = [b for b in builds if b.name == self.build_name]
            while len(filtered_builds) < 1:
                offset += 20
                builds = BuildsApi.recent_builds(20, offset)
                if len(builds) == 0:
                    raise Exception()
                filtered_builds = [b for b in builds if b.name == self.build_name]
            self._build = filtered_builds[0]
        return self._build

    @property
    def project(self):
        if self._project is None:
            offset = 0
            projects = ProjectsApi.recent_projects(20, offset)
            filtered_projects = [p for p in projects if p.name == self.project_name]
            while len(filtered_projects) < 1:
                offset += 20
                projects = ProjectsApi.recent_projects(20, offset)
                if len(projects) == 0:
                    raise Exception()
                filtered_projects = [p for p in projects if p.name == self.project_name]
            self._project = filtered_projects[0]
        return self._project

    @staticmethod
    def by_id(session_id=None):
        """
        Get the Session for the given ID

        Example::

            driver = webdriver.Remote(url, desired_caps)
            session_id = driver.session_id
            driver.quit()

            session = Session.by_id(session_id)

        :param str session_id: Unique Session ID
        :return: :class:`bsapi.app_automate.appium.sessions.Session`
        """
        if session_id is None:
            raise ValueError("Session ID is required")

        session = SessionsApi.details(session_id)
        return session

    def get_session_logs(self):
        """
        Get the Session logs from BrowserStack

        Example::

            session = Session.by_id(session_id)
            with open("session.log", "wb") as f:
                with session.get_logs() as r:
                    f.write(r.content)


        :return: Response object containing the session logs from BrowserStack
        :rtype: requests.Response
        """
        response = Api.http.get(self.logs, stream=True, **Settings.request())
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def save_session_logs(self, filename=None):
        """
        Download the session logs from BrowserStack to the file name

        Example::

            session = Session.by_id(session_id)
            session.save_session_logs("session.log")

        :param filename: File name for the logs to be saved to
        :return: None
        """
        if filename is None:
            raise ValueError("File name is required")

        with open(filename, "wb") as f:
            with self.get_session_logs() as response:
                f.write(response.content)

    def get_appium_logs(self):
        """
        Get the Appium logs from BrowserStack for the Session

        Example::

            session = Session.by_id(session_id)
            with session.get_appium_logs() as response:
                with open("appium.log", "wb") as f:
                    f.write(response.content)

        :return: Response object containing the Appium Logs
        :rtype: requests.Response
        """
        response = Api.http.get(self.appium_logs_url, stream=True, **Settings.request())
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def save_appium_logs(self, filename=None):
        """
        Save the appium logs to the file system

        Example::

            session = Session.by_id(session_id)
            session.save_appium_logs("appium.log")

        :param filename:
        """
        if filename is None:
            raise ValueError("File name is required")

        with self.get_appium_logs() as response:
            with open(filename, "wb") as f:
                f.write(response.content)

    def get_device_logs(self):
        """
        Get the Appium logs from BrowserStack for the Session

        Example::

            session = Session.by_id(session_id)
            with session.get_device_logs() as response:
                with open("device.log", "wb") as f:
                    f.write(response.content)

        :return: Response object containing the Device logs from BrowserStack
        :rtype: requests.Response

        """
        response = Api.http.get(self.device_logs_url, stream=True, **Settings.request())
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def save_device_logs(self, filename=None):
        """
        Save the device logs to the file system

        Example::

            session = Session.by_id(session_id)
            session.save_device_logs("device.log")

        :param filename:
        """
        if filename is None:
            raise ValueError("File name is required")

        with self.get_device_logs() as response:
            with open(filename, "wb") as f:
                f.write(response.content)

    def get_network_logs(self):
        """
        Get the Network logs from BrowserStack for the Session

        Example::

            session = Session.by_id(session_id)
            with session.get_network_logs() as response:
                with open("network.log", "wb") as f:
                    f.write(response.content)

        :return: Response object containing the Network logs for BrowserStack
        :rtype: requests.Response
        """
        response = SessionsApi.get_network_logs(self.build.hashed_id, self.hashed_id)
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def save_network_logs(self, filename=None):
        """
        Save the network logs to the file system

        Example::

            session = Session.by_id(session_id)
            session.save_network_logs("network.log")

        :param filename:
        """
        if filename is None:
            raise ValueError("File name is required")

        with self.get_network_logs() as response:
            with open(filename, "wb") as f:
                f.write(response.content)

    def get_video(self):
        """
        Get the video from BrowserStack for the Session

        Example::

            session = Session.by_id(session_id)
            with session.get_video() as response:
                with open("BrowserStack.mp4", "wb") as f:
                    f.write(response.content)

        :return: Response object containing the Video recording for the BrowserStack session
        :rtype: requests.Response
        """
        response = Api.http.get(self.video_url, stream=True, **Settings.request())
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def save_video(self, filename=None):
        """
        Save the video of the session to the file system

        Example::

            session = Session.by_id(session_id)
            session.save_video("BrowserStack.mp4")


        :param filename:
        """
        if filename is None:
            raise ValueError("File name is required")

        with self.get_video() as response:
            with open(filename, "wb") as f:
                f.write(response.content)


class AppProfilingData:
    """
    App profiling data entry

    :param str timestamp:
    :param str cpu:
    :param str memory:
    :param str memory_available:
    :param str battery:
    :param str temperature:
    """
    def __init__(self, ts=None, cpu=None, mem=None, mema=None, batt=None,
                 temp=None):
        self.timestamp = ts
        self.cpu = cpu
        self.memory = mem
        self.memory_available = mema
        self.battery = batt
        self.temperature = temp


class SessionsApi(Api):
    """
    Wrapper around the Sessions endpoint
    """
    @classmethod
    def details(cls, session_id=None):
        """
        Get the details for a session provided the ID

        Example::

            session = SessionsApi.details(session_id)


        :param session_id: the hashed id for the session
        :return: Session Object
        :rtype: :class:`bsapi.app_automate.appium.sessions.Session`
        """
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
        """
        Update the status of a session

        Example::

            session = SessionsApi(session_id, SessionStatus.passed)

        :param session_id: The session id
        :param status: The new status. Use :class:`SessionStatus` for available statuses
        :type status: str
        :param reason: reason for the new status
        :return: Updated Session object
        """
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
        """
        Delete the session from BrowserStack

        Example::

            response = SessionApi.delete(session_id)
            if response.status == "ok":
                print("The session has been deleted")

        :param session_id: The unique id for the session
        :return: delete status message
        :rtype: :class:`bsapi.app_automate.appium.responses.DeleteResponse`
        """
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
        """
        Get the BrowserStack logs for the session

        Example::

            with SessionsApi.get_text_logs(build_id, session_id) as response:
                with open("session.log", "w") as f:
                    f.write(response.content)

        :param build_id: the unique build id
        :param session_id: the unique session id
        :return: returns the raw response object for the request
        :rtype: requests.Response
        """
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
        """
        Get the device logs from BrowserStack

        Example::

            with SessionsApi.get_device_logs(build_id, session_id) as response:
                with open("device.log", "w") as f:
                    f.write(response.content)

        :param build_id: The build id
        :param session_id: the session id
        :return: returns the raw response object for the request
        :rtype: requests.Response
        """
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
        """
        Get the Appium logs from BrowserStack

        Example::

            with SessionsApi.get_appium_logs(build_id, session_id) as response:
                with open("appium.log", "w") as f:
                    f.write(response.content)

        :param build_id: The build id
        :param session_id: The session id
        :return: The raw response object from the request
        :rtype: requests.Response
        """
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
        """
        Get the network logs from BrowserStack

        Example::

            with SessionsApi.get_network_logs(build_id, session_id) as response:
                with open("network.json", "w") as f:
                    f.write(response.content)

        :param build_id: The build id
        :param session_id: The session id
        :return: The raw response object from the request
        :rtype: requests.Response
        """
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
        """
        Get the profiling data from BrowserStack

        Example::

            profiling_data = SessionsApi.get_profiling_data(build_id, session_id)
            for data_entry in profiling_data:
                print(data_entry.mem)

        :param build_id: The Build ID
        :param session_id: The Session ID
        :return: returns a list of profiling data entries
        :rtype: list[:class:`bsapi.app_automate.appium.sessions.AppProfilingData`]
        """
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










