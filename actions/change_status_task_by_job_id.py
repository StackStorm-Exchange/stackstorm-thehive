import requests
from thehive4py.api import TheHiveApi
from st2common.runners.base_action import Action
from thehive4py.models import CaseTask
from thehive4py.exceptions import CaseTaskException


class TheHiveApiExtended(TheHiveApi):
    def get_task(self, task_id):
        req = self.url + "/api/case/task/{}".format(task_id)
        try:
            return requests.get(req, proxies=self.proxies, auth=self.auth, verify=self.cert)
        except requests.exceptions.RequestException as e:
            raise CaseTaskException("Case task logs search error: {}".format(e))


__all__ = [
    'ChangeStatusTaskByJobIdAction'
]


class ChangeStatusTaskByJobIdAction(Action):
    def run(self, job_id, status):
        task_id = self.action_service.get_value(name='thehive_job_{}'.format(job_id), local=False)

        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.get_task(task_id)
        if response.status_code == 200:
            task_object = response.json()
            task = CaseTask(json=task_object)
            task.id = task_id
            task.status = status
            task.owner = self.config['thehive_bot_username']
            api.update_case_task(task)
            if status == 'Completed':
                self.action_service.delete_value(name='thehive_job_{}'.format(job_id), local=False)
        else:
            raise ValueError('[ChangeStatusTaskByJobIdAction]: status_code %d'
                 % response.status_code)

        return True
