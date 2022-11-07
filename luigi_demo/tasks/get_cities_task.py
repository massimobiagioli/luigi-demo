from luigi_demo.common.base_task import BaseTask
from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.common.task_exception import TaskException
from luigi_demo.common.task_result import create_success_result, create_error_result
from luigi_demo.services.get_cities import get_cities


class GetCitiesTask(BaseTask):
    retry_count = 3
    retries = 0

    def output(self):
        return self.get_output_target(
            target=OutputTargetEnum.LOCAL,
            path="out/cities.json"
        )

    def run(self):
        self.retries += 1
        if self.retries == self.retry_count:
            output_data = create_error_result(
                TaskException(
                    message="Error retrieving cities",
                    task_name=self.task_family,
                )
            )
            self.write_output(
                data=output_data
            )

        cities = get_cities()
        output_data = create_success_result(
            data=cities
        )
        self.write_output(
            data=output_data
        )
