from thehive4py.api import TheHiveApi
from thehive4py.query import *
from st2reactor.sensor.base import PollingSensor

__all__ = [
    'TheHiveTasksSearchSensor'
]

class TheHiveTasksSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(TheHiveTasksSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'thehive.new_task'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._client = TheHiveApi(self._config['thehive_url'], self._config['thehive_api_key'])

    def poll(self):
        response = self._client.find_tasks(query=And(Eq('owner', self._config['thehive_bot_username']), Eq('status', 'Waiting')))

        if response.status_code == 200:
            tasks = response.json()
            self._logger.debug('%d tasks found'%len(tasks))
            for task in tasks:
                self._logger.debug('New task %s'%task['title'])
                self._sensor_service.dispatch(trigger=self._trigger_ref, payload=task)
        else:
            self._logger.exception('TheHive sensor failed with status_code %d'%response.status_code)
            raise ValueError('[TheHiveTasksSearchSensor]: status_code %d'%response.status_code)


    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
