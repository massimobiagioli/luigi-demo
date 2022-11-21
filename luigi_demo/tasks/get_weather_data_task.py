from datetime import datetime

from luigi_demo.common.base_task import BaseTask
from luigi_demo.services.get_weather_data import get_weather_data
from luigi_demo.tasks.get_cities_task import GetCitiesTask


class GetWeatherDataTask(BaseTask):
    retry_count = 3

    def requires(self):
        return GetCitiesTask(
            debug=self.debug,
            nonce=self.nonce,
        )

    def run(self):
        now = datetime.now()
        cities_result = self.read_input()
        self.write_output(
            data=get_weather_data(
                detection_date=now, detection_hour=now.hour, cities=cities_result
            )
        )
