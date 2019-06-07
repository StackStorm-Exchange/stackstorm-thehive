import random
import requests
from thehive4py.api import TheHiveApi
from thehive4py.query import Eq
from st2common.runners.base_action import Action


class TheHiveApiExtended(TheHiveApi):
    def get_analyzer_by_name_and_data_type(self, name, data_type):
        req = self.url + "/api/connector/cortex/analyzer/type/{}".format(data_type)
        analyzers = requests.get(req, proxies=self.proxies, auth=self.auth, verify=self.cert)
        analyzer = [a for a in analyzers.json() if a['name'].lower() == name.lower()]
        return analyzer[0]


__all__ = [
    'RunAnalyzerOnDataTypeAction'
]


class RunAnalyzerOnDataTypeAction(Action):
    def run(self, case_id, data_type, analyzer_name, linked_task_name=None):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        linked_task_id = None
        if linked_task_name:
            response = api.get_case_tasks(case_id, query=Eq('title', linked_task_name))
            if response.status_code == 200:
                tasks = response.json()
                if len(tasks) == 1:
                    linked_task_id = tasks[0]['id']
                else:
                    raise ValueError('[RunAnalyzerOnDataTypeAction]: task not found')
            else:
                raise ValueError('[RunAnalyzerOnDataTypeAction]: tasks status_code %d'
                     % response.status_code)

        analyzer = api.get_analyzer_by_name_and_data_type(analyzer_name, data_type)
        response = api.get_case_observables(case_id, query=Eq('dataType', data_type))
        if response.status_code == 200:
            observables = response.json()
            if len(observables) == 1:
                for observable in observables:
                    cortex_id = random.choice(analyzer['cortexIds'])
                    response_job = api.run_analyzer(cortex_id, observable['id'], analyzer['id'])
                    if response_job.status_code == 200:
                        job = response_job.json()
                        if linked_task_id:
                            self.action_service.set_value(
                                name='thehive_job_{}'.format(job['id']),
                                value=linked_task_id,
                                local=False
                            )
                        return job
                    else:
                        raise ValueError('[RunAnalyzerOnDataTypeAction]: job status_code %d'
                             % response.status_code)
            else:
                raise ValueError('[RunAnalyzerOnDataTypeAction]: no observable')
        else:
            raise ValueError('[RunAnalyzerOnDataTypeAction]: status_code %d' % response.status_code)
