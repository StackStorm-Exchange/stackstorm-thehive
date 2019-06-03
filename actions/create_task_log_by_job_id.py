from thehive4py.api import TheHiveApi
from st2common.runners.base_action import Action

__all__ = [
    'CreateTaskLogByJobIdAction'
]


class CreateTaskLogByJobIdAction(Action):
    def run(self, job_id, log):
        api = TheHiveApi(self.config['thehive_url'], self.config['thehive_api_key'])
        task_id = self.action_service.get_value(name='thehive_job_{}'.format(job_id), local=False)
        response = api.create_task_log(task_id, log)

        return response.json()
