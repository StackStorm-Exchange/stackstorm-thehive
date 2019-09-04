from thehive4pyextended import TheHiveApiExtended
from st2common.runners.base_action import Action
from thehive4py.models import CaseTask

__all__ = [
    'ChangeStatusTaskAction'
]


class ChangeStatusTaskAction(Action):
    def run(self, task_id, status):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.get_task(task_id)
        if response.status_code == 200:
            task_object = response.json()
            task = CaseTask(json=task_object)
            task.id = task_id
            task.status = status
            task.owner = self.config['thehive_bot_username']
            api.update_case_task(task)
        else:
            raise ValueError('[ChangeStatusTaskAction]: status_code %d' % response.status_code)

        return True
