from datetime import datetime

from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.common.task_exception import TaskException
from luigi_demo.common.task_result import create_success_result, create_error_result
from luigi_demo.services.get_weather_data import get_weather_data
from luigi_demo.tasks.get_cities_task import GetCitiesTask


class GetWeatherDataTask(BaseTask):
    retry_count = 3
    retries = 0

    def requires(self):
        return GetCitiesTask()

    def output(self):
        now = datetime.now().strftime('%Y%m%d_%H')
        return self.get_output_target(
            target=OutputTargetEnum.LOCAL,
            path=f'out/weather-data-{now}.json'
        )

    def run(self):
        cities_result = self.read_input()
        if not cities_result.is_success():
            self.write_output(
                data=cities_result
            )
            return

        self.retries += 1
        if self.retries == self.retry_count:
            output_data = create_error_result(
                TaskException(
                    message="Error retrieving weather data",
                    task_name=self.task_family,
                )
            )
            self.write_output(
                data=output_data
            )

        weather_data = get_weather_data(cities_result.data)
        self.write_output(
            create_success_result(
                data=weather_data
            )
        )
