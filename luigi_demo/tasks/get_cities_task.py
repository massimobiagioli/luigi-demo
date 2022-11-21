from luigi_demo.common.base_task import BaseTask
from luigi_demo.services.get_cities import get_cities


class GetCitiesTask(BaseTask):
    retry_count = 3

    def run(self):
        self.write_output(data=get_cities())
