from thehive4py.api import TheHiveApi
from thehive4py.models import CaseTaskLog
from st2common.runners.base_action import Action

__all__ = [
    'CreateTaskLogAction'
]


class CreateTaskLogAction(Action):
    def run(self, task_id, log):
        api = TheHiveApi(self.config['thehive_url'], self.config['thehive_api_key'])
        case_task_log = CaseTaskLog(message=log)
        response = api.create_task_log(task_id, case_task_log)

        return response.json()
