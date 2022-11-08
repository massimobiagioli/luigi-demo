from datetime import datetime

from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.common.task_exception import TaskException
from luigi_demo.common.task_result import create_success_result, create_error_result
from luigi_demo.services.store_weather_data import store_weather_data
from luigi_demo.tasks.get_weather_data_task import GetWeatherDataTask


class StoreWeatherDataTask(BaseTask):
    retry_count = 3
    retries = 0

    def requires(self):
        return GetWeatherDataTask(
            debug=self.debug,
            nonce=self.nonce,
        )

    def output(self):
        now = datetime.now().strftime('%Y%m%d_%H')
        return self.get_output_target(
            target=OutputTargetEnum.LOCAL,
            path=f'out/store-weather-data-{self.nonce}-{now}.json'
        )

    def run(self):
        weather_data_result = self.read_input()
        if not weather_data_result.is_success():
            self.write_output(
                data=weather_data_result
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
            return

        store_weather_data(weather_data_result.data)
        self.write_output(
            create_success_result()
        )
