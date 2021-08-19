from bsapi import Settings, Api


class AppAutomatePlan:
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

    @classmethod
    def details(cls):
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
