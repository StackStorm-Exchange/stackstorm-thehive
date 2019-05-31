from thehive4py.api import TheHiveApi
from st2common.runners.base_action import Action
from thehive4py.query import *
from thehive4py.models import CaseTask

__all__ = [
    'TakeTaskAction'
]

class TakeTaskAction(Action):
    def run(self, task_id):
        api = TheHiveApi(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.find_tasks(query=Eq('_id', task_id))
        if response.status_code == 200:
            tasks = response.json()
            if len(tasks) == 1:
                task = CaseTask(json=tasks[0])
                task.id = task_id
                task.status = 'InProgress'
                task.owner = self.config['thehive_bot_username']
                api.update_case_task(task)
            else:
                raise ValueError('[TakeTaskAction]: no tasks with this id')
        else:
            raise ValueError('[TakeTaskAction]: status_code %d'%response.status_code)

        return True
