from thehive4pyextended import TheHiveApiExtended
from st2common.runners.base_action import Action
from thehive4py.models import CaseTask
from thehive4py.query import Eq

__all__ = [
    'ChangeStatusTaskByNameAction'
]


class ChangeStatusTaskByNameAction(Action):
    def run(self, case_id, task_name, status):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])

        response = api.get_case_tasks(case_id, query=Eq('title', task_name))
        if response.status_code == 200:
            tasks = response.json()
            if len(tasks) == 1:
                task_id = tasks[0]['id']
            else:
                raise ValueError('[ChangeStatusTaskByNameAction]: task not found')
        else:
            raise ValueError('[ChangeStatusTaskByNameAction]: tasks status_code %d'
                 % response.status_code)

        response = api.get_task(task_id)
        if response.status_code == 200:
            task_object = response.json()
            task = CaseTask(json=task_object)
            task.id = task_id
            task.status = status
            task.owner = self.config['thehive_bot_username']
            api.update_case_task(task)
        else:
            raise ValueError('[ChangeStatusTaskByNameAction]: status_code %d'
                 % response.status_code)

        return True
