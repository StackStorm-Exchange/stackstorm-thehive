from thehive4py.api import TheHiveApi
from st2common.runners.base_action import Action

__all__ = [
    'CreateTaskLogAction'
]


class CreateTaskLogAction(Action):
    def run(self, task_id, log):
        api = TheHiveApi(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.create_task_log(task_id, log)

        return response.json()
