from datetime import datetime

from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
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
        now = datetime.now().strftime("%Y%m%d_%H")
        return self.get_output_target(
            target=OutputTargetEnum.LOCAL,
            path=f"out/store-weather-data-{self.nonce}-{now}.json",
        )

    def run(self):
        store_weather_data(self.read_input())
        # TODO: Add report
        self.write_output([])
