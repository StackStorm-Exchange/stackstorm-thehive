from time import time
from thehive4py.api import TheHiveApi
from thehive4py.query import Gte
from st2reactor.sensor.base import PollingSensor

__all__ = [
    'TheHiveAlertsSearchSensor'
]


class TheHiveAlertsSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(TheHiveAlertsSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'thehive.new_alert'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._client = TheHiveApi(self._config['thehive_url'], self._config['thehive_api_key'])
        self._last_run_time = int((time() - 60 * 3) * 1000)

    def poll(self):
        last_run_time = self._get_last_run_time()
        self._reset_last_run_time()
        response = self._client.find_alerts(query=Gte('createdAt', last_run_time))

        if response.status_code == 200:
            alerts = response.json()
            self._logger.debug('%d alerts found (%d)' % (len(alerts), last_run_time))
            for alert in alerts:
                self._logger.debug('New alert %s' % alert['title'])
                self._sensor_service.dispatch(trigger=self._trigger_ref, payload=alert)
        else:
            self._logger.exception('TheHive sensor failed with status_code %d'
                 % response.status_code)
            raise ValueError('[TheHiveAlertsSearchSensor]: status_code %d' % response.status_code)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_run_time(self):
        if not self._last_run_time and hasattr(self._sensor_service, 'get_value'):
            self._last_run_time = self._sensor_service.get_value(name='last_run_time')

        return self._last_run_time

    def _reset_last_run_time(self):
        self._last_run_time = int(time() * 1000)

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='last_run_time', value=self._last_run_time)
