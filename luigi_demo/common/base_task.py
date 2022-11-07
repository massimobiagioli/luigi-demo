import json
import logging
import uuid

import luigi
from luigi.mock import MockTarget

from luigi_demo.common.output_target_enum import OutputTargetEnum
from luigi_demo.common.task_result import TaskResult

LUIGI_LOGGER_NAME = 'luigi-interface'


class BaseTask(luigi.Task):
    logger = logging.getLogger(LUIGI_LOGGER_NAME)

    debug = luigi.BoolParameter(
        default=False,
        parsing=luigi.BoolParameter.EXPLICIT_PARSING)

    nonce = luigi.Parameter(
        default=str(uuid.uuid4())
    )

    def get_output_target(self, target, **kwargs):
        if self.debug:
            return MockTarget(self.debug_output_name)

        if target == OutputTargetEnum.LOCAL:
            return luigi.LocalTarget(**kwargs)

    def read_input(self):
        with self.input().open('r') as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                self.logger.error('Could not decode input file')
                return []

    def write_output(self, data: TaskResult):
        with self.output().open('w') as f:
            f.write(f"{json.dumps(data.serialize(), indent=4)}\n")

    @property
    def debug_output_name(self):
        return f'out/{self.task_namespace}_{self.task_family}_{self.task_id}.json'
