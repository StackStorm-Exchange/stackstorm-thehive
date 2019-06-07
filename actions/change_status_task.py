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
