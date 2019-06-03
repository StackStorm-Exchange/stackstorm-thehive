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
    'RunAnalyzerAction'
]


class RunAnalyzerAction(Action):
    def run(self, case_id, analyzer_name, data_type):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        analyzer = api.get_analyzer_by_name_and_data_type(analyzer_name, data_type)
        response = api.get_case_observables(case_id, query=Eq('dataType', data_type))
        if response.status_code == 200:
            observables = response.json()
            for observable in observables:
                cortex_id = random.choice(analyzer['cortexIds'])
                api.run_analyzer(cortex_id, observable['id'], analyzer['id'])
        else:
            raise ValueError('[RunAnalyzerAction]: status_code %d' % response.status_code)
        return True
