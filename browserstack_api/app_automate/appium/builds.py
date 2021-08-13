
class Build:
    def __init__(self, build_id=None, name=None, duration=None, status=None, tags=None,
                 group_id=None, user_id=None, automation_project_id=None, created_at=None,
                 updated_at=None, hashed_id=None, delta=None, test_data=None,
                 sub_group_id=None):
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
        self.test_data = test_data
        self.sub_group_id = sub_group_id
