import json
import logging
import uuid

import luigi
from luigi import Target
from luigi.mock import MockTarget

from luigi_demo.common.task_result import TaskResultData

LUIGI_LOGGER_NAME = "luigi-interface"


class BaseTask(luigi.Task):
    logger = logging.getLogger(LUIGI_LOGGER_NAME)

    debug = luigi.BoolParameter(
        default=False, parsing=luigi.BoolParameter.EXPLICIT_PARSING
    )

    nonce = luigi.Parameter(default=str(uuid.uuid4()))

    def output(self) -> Target:
        return self.get_output_target(path=self.output_name)

    def get_output_target(self, **kwargs) -> Target:
        if self.debug:
            return MockTarget(self.output_name)
        return luigi.LocalTarget(**kwargs)

    def read_input(self) -> TaskResultData:
        with self.input().open("r") as f:
            return json.load(f)

    def write_output(self, data: TaskResultData) -> None:
        with self.output().open("w") as f:
            f.write(f"{json.dumps(data, indent=4)}\n")

    @property
    def output_name(self):
        return f"out/{self.task_family}_{self.task_id}.json"
