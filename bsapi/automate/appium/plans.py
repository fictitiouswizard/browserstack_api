from bsapi import Settings, Api
from bsapi.models import AutomatePlan


class PlansApi(Api):
    """Class for interacting with the Automate Plans REST endpoint on BrowserStack"""

    @classmethod
    def details(cls):
        """
        Get the plan details for the current user

        Example::

            plan = PlansApi.details()

        :return: The plan details for the current user
        :rtype: :class:`bsapi.models.AutomatePlan`
        """
        url = f"{Settings.base_url}/automate/plan.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return AutomatePlan(
                automate_plan=rj["automate_plan"],
                parallel_sessions_running=rj["parallel_sessions_running"],
                team_parallel_sessions_max_allowed=rj["team_parallel_sessions_max_allowed"],
                parallel_sessions_max_allowed=rj["parallel_sessions_max_allowed"],
                queued_sessions=rj["queued_sessions"],
                queued_sessions_max_allowed=rj["queued_sessions_max_allowed"]
            )
        else:
            response.raise_for_status()