from bsapi import Settings, Api


class AppAutomatePlan:
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


class PlansApi(Api):
    """Class for interacting with the Plans REST endpoint on BrowserStack"""

    @classmethod
    def details(cls):
        """
        Get the plan details for the current user

        Example::

            plan = PlansApi.details()

        :return: The plan details for the current user
        :rtype: :class:`bsapi.app_automate.appium.plans.AppAutomatePlan`
        """
        url = f"{Settings.base_url}/app-automate/plan.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return AppAutomatePlan(
                automate_plan=rj["automate_plan"],
                parallel_sessions_running=rj["parallel_sessions_running"],
                team_parallel_sessions_max_allowed=rj["team_parallel_sessions_max_allowed"],
                parallel_sessions_max_allowed=rj["parallel_sessions_max_allowed"],
                queued_sessions=rj["queued_sessions"],
                queued_sessions_max_allowed=rj["queued_sessions_max_allowed"]
            )
        else:
            response.raise_for_status()
