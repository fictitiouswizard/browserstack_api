
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
