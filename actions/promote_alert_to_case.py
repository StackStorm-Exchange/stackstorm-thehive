import requests
import json
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import AlertException
from st2common.runners.base_action import Action


class TheHiveApiExtended(TheHiveApi):
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


__all__ = [
    'PromoteAlertToCaseAction'
]


class PromoteAlertToCaseAction(Action):
    def run(self, alert_id, case_template=None):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.promote_alert_to_case(alert_id, case_template)

        return response.json()
