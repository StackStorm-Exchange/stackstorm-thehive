from st2common.runners.base_action import Action
from thehive4pyextended import TheHiveApiExtended

__all__ = [
    'PromoteAlertToCaseAction'
]


class PromoteAlertToCaseAction(Action):
    def run(self, alert_id, case_template=None):
        api = TheHiveApiExtended(self.config['thehive_url'], self.config['thehive_api_key'])
        response = api.promote_alert_to_case(alert_id, case_template)

        return response.json()
