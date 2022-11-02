from datetime import datetime
import json
from dataclasses import asdict
import luigi
from luigi_demo.services.get_weather_data import get_weather_data


class WeatherForecastTask(luigi.Task):
    def output(self):
        now = datetime.now().strftime('%Y%m%d_%H%M')
        return luigi.LocalTarget(f'out/weather-forecast-{now}.txt')

    def run(self):
        weather_data = get_weather_data(['Milano', 'Torino', 'Roma', 'Napoli', 'Palermo'])

        with self.output().open("w") as outfile:
            outfile.write(f"{json.dumps({'cities': weather_data}, default=asdict, indent=4)}\n")
