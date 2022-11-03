import json
import luigi

from luigi_demo.services.get_cities import get_cities


class GetCitiesTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(f'out/cities.txt')

    def run(self):
        cities = get_cities()

        with self.output().open("w") as outfile:
            outfile.write(f"{json.dumps(cities, indent=4)}\n")
