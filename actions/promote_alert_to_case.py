from thehive4py.api import TheHiveApi
from st2common.runners.base_action import Action

__all__ = [
    'PromoteAlertToCaseAction'
]

class PromoteAlertToCaseAction(Action):
    def run(self, alert_id, case_template = None):
        api = TheHiveApi(self.config['thehive_url'], self.config['thehive_api_key'])
        # api.promote_alert_to_case(alert_id, case_template) wait for https://github.com/TheHive-Project/TheHive4py/pull/115
        api.promote_alert_to_case(alert_id)

        return True
