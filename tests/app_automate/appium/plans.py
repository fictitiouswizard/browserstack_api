import unittest

from bsapi.app_automate.appium.plans import PlansApi


class TestPlansApi(unittest.TestCase):

    def test_details(self):
        plan = PlansApi.details()
        self.assertEqual(plan.automate_plan, "App Automate")
        self.assertEqual(5, plan.parallel_sessions_max_allowed)


if __name__ == "__main__":
    unittest.main()
