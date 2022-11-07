import json
from dataclasses import asdict
from datetime import datetime

from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.services.get_weather_data import get_weather_data
from luigi_demo.tasks.get_cities_task import GetCitiesTask


class GetWeatherDataTask(BaseTask):
    def requires(self):
        return GetCitiesTask()

    def output(self):
        now = datetime.now().strftime('%Y%m%d_%H')
        return self.get_output_target(OutputTargetEnum.LOCAL, path=f'out/weather-data-{now}.json')

    def run(self):
        with self.input().open('r') as f:
            cities = json.load(f)

        weather_data = get_weather_data(cities)

        with self.output().open("w") as outfile:
            outfile.write(f"{json.dumps({'cities': weather_data}, default=asdict, indent=4)}\n")
