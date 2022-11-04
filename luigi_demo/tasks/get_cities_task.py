import json

from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_targets import OutputTargetsEnum
from luigi_demo.services.get_cities import get_cities


class GetCitiesTask(BaseTask):
    retry_count = 3

    def output(self):
        return self.get_output(OutputTargetsEnum.local, path="out/cities.json")

    def run(self):
        cities = get_cities()

        with self.output().open("w") as outfile:
            outfile.write(f"{json.dumps(cities, indent=4)}\n")
