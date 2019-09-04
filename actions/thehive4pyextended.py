import requests
import json
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import CaseTaskException, AlertException


class TheHiveApiExtended(TheHiveApi):
    def get_task(self, task_id):
        req = self.url + "/api/case/task/{}".format(task_id)
        try:
            return requests.get(req, proxies=self.proxies, auth=self.auth, verify=self.cert)
        except requests.exceptions.RequestException as e:
            raise CaseTaskException("Case task logs search error: {}".format(e))

    def get_analyzer_by_name_and_data_type(self, name, data_type):
        req = self.url + "/api/connector/cortex/analyzer/type/{}".format(data_type)
        analyzers = requests.get(req, proxies=self.proxies, auth=self.auth, verify=self.cert)
        analyzer = [a for a in analyzers.json() if a['name'].lower() == name.lower()]
        return analyzer[0]

    def promote_alert_to_case(self, alert_id, case_template=None):
        """
            This uses the TheHiveAPI to promote an alert to a case
            :param alert_id: Alert identifier
            :param case_template: Optional Case Template name
            :return: TheHive Case
            :rtype: json
        """

        req = self.url + "/api/alert/{}/createCase".format(alert_id)

        try:
            return requests.post(req, headers={'Content-Type': 'application/json'},
                                 proxies=self.proxies, auth=self.auth,
                                 verify=self.cert, data=json.dumps({"caseTemplate": case_template}))

        except requests.exceptions.RequestException as the_exception:
            raise AlertException("Couldn't promote alert to case: {}".format(the_exception))

        return None
