from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.common.task_result import create_success_result
from luigi_demo.services.get_cities import get_cities


class GetCitiesTask(BaseTask):
    retry_count = 3

    def output(self):
        return self.get_output_target(OutputTargetEnum.LOCAL, path="out/cities.json")

    def run(self):
        cities = get_cities()
        output_data = create_success_result(cities)

        self.write_output(output_data)
