from luigi_demo.common.base_task import BaseTask
from luigi_demo.services.store_weather_data import store_weather_data
from luigi_demo.tasks.get_weather_data_task import GetWeatherDataTask


class StoreWeatherDataTask(BaseTask):
    retry_count = 3

    def requires(self):
        return GetWeatherDataTask(
            debug=self.debug,
            nonce=self.nonce,
        )

    def run(self):
        weather_data = self.read_input()
        store_weather_data(weather_data)
        self.write_output({"processed": len(weather_data)})
