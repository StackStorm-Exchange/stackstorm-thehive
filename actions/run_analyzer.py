import random
from thehive4pyextended import TheHiveApiExtended
from thehive4py.query import Id, Eq
from st2common.runners.base_action import Action

__all__ = [
    'RunAnalyzerAction'
]


class RunAnalyzerAction(Action):
    def run(self, case_id, artifact_id, analyzer_name, linked_task_name=None):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        linked_task_id = None
        if linked_task_name:
            response = api.get_case_tasks(case_id, query=Eq('title', linked_task_name))
            if response.status_code == 200:
                tasks = response.json()
                if len(tasks) == 1:
                    linked_task_id = tasks[0]['id']
                else:
                    raise ValueError('[RunAnalyzerAction]: task not found')
            else:
                raise ValueError('[RunAnalyzerAction]: tasks status_code %d' % response.status_code)

        response = api.get_case_observables(case_id, query=Id(artifact_id))
        if response.status_code == 200:
            observables = response.json()
            if len(observables) == 1:
                observable = observables[0]
                analyzer = api.get_analyzer_by_name_and_data_type(
                    analyzer_name, observable['dataType']
                )

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
                    raise ValueError('[RunAnalyzerAction]: job status_code %d'
                         % response.status_code)
            else:
                raise ValueError('[RunAnalyzerAction]: no observable')
        else:
            raise ValueError('[RunAnalyzerAction]: status_code %d' % response.status_code)
