from dataclasses import dataclass, asdict
from typing import Union

from luigi_demo.common.status_enum import StatusEnum
from luigi_demo.common.task_exception import TaskException

TaskResultData = Union[dict, list, str, None]


@dataclass
class TaskResult:
    status: StatusEnum
    data: TaskResultData

    def serialize(self):
        return asdict(self)


def create_success_result(data: TaskResultData):
    return TaskResult(StatusEnum.SUCCESS, data)


def create_error_result(error: TaskException):
    return TaskResult(
        StatusEnum.ERROR,
        {
            "message": str(error),
            "task_name": error.task_name,
        }
    )
