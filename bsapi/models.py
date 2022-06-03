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
    :var str framework:
    """

    def __init__(self, build_id=None, name=None, duration=None, status=None, tags=None,
                 group_id=None, user_id=None, automation_project_id=None, created_at=None,
                 updated_at=None, hashed_id=None, delta=None, test_data=None,
                 sub_group_id=None, framework=None):
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
        self.sub_group_id = sub_group_id
        self.framework = framework
        self.test_data = test_data

    @classmethod
    def from_dict(cls, b):
        build = cls()
        build.build_id = b["id"]
        build.name = b["name"]
        build.duration = b["duration"]
        build.status = b["status"]
        build.tags = b["tags"]
        build.group_id = b["group_id"]
        build.user_id = b["user_id"]
        build.automation_project_id = b["automation_project_id"]
        build.created_at = b["created_at"]
        build.updated_at = b["updated_at"]
        build.hashed_id = b["hashed_id"]
        build.delta = b["delta"]
        build.sub_group_id = b["sub_group_id"]
        build.framework = b["framework"]
        build.test_data = b["test_data"]
        return build


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

    @classmethod
    def from_dict(cls, p):
        project = cls()
        project.project_id = p["id"] if "id" in p else None
        project.name = p["name"] if "name" in p else None
        project.group_id = p["group_id"] if "group_id" in p else None
        project.user_id = p["user_id"] if "user_id" in p else None
        project.created_at = p["created_at"] if "created_at" in p else None
        project.updated_at = p["updated_at"] if "updated_at" in p else None
        project.sub_group_id = p["sub_group_id"] if "sub_group_id" in p else None
        return project


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
