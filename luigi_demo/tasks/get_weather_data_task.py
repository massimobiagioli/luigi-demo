from datetime import datetime
import json
from dataclasses import asdict
import luigi
from luigi_demo.services.get_weather_data import get_weather_data
from luigi_demo.tasks.get_cities import GetCitiesTask


class GetWeatherDataTask(luigi.Task):
    def requires(self):
        return GetCitiesTask()

    def output(self):
        now = datetime.now().strftime('%Y%m%d_%H')
        return luigi.LocalTarget(f'out/weather-data-{now}.txt')

    def run(self):
        with self.input().open('r') as f:
            cities = json.load(f)

        weather_data = get_weather_data(cities)

        with self.output().open("w") as outfile:
            outfile.write(f"{json.dumps({'cities': weather_data}, default=asdict, indent=4)}\n")
