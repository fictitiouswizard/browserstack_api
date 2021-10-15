class AutomatePlan:
    """
    Plan information for the current user

    :param str automate_plan:
    :param str parallel_sessions_running:
    :param str team_parallel_sessions_max_allowed:
    :param str parallel_sessions_max_allowed:
    :param str queued_sessions:
    :param str queued_sessions_max_allowed:
    """
    def __init__(self, automate_plan=None, parallel_sessions_running=None,
                 team_parallel_sessions_max_allowed=None,
                 parallel_sessions_max_allowed=None,
                 queued_sessions=None, queued_sessions_max_allowed=None):
        self.automate_plan = automate_plan
        self.parallel_sessions_running = parallel_sessions_running
        self.team_parallel_sessions_max_allowed = team_parallel_sessions_max_allowed
        self.parallel_sessions_max_allowed = parallel_sessions_max_allowed
        self.queued_sessions = queued_sessions
        self.queued_sessions_max_allowed = queued_sessions_max_allowed


class Browser:
    """
    Browser supported by BrowserStack

    :param str browser_os:
    :param str os_version:
    :param str browser:
    :param str device:
    :param str browser_version:
    :param bool real_mobile:
    """
    def __init__(self, browser_os=None, os_version=None, browser=None,
                 device=None, browser_version=None, real_mobile=None):
        self.browser_os = browser_os
        self.os_version = os_version
        self.browser = browser
        self.device = device
        self.browser_version = browser_version
        self.real_mobile = real_mobile


class DeleteResponse:
    """
    Response for delete requests sents to BrowserStack

    :param str status: Status of the delete request
    :param str message: Message from the server
    """
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message

    @staticmethod
    def from_dict(d):
        return DeleteResponse(
            status=d["status"] if "status" in d else None,
            message=d["message"] if "message" in d else None
        )
