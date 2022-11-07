import json
import uuid

import pytest
from luigi.mock import MockTarget

from luigi_demo.tasks.get_cities_task import GetCitiesTask


def test_get_cities_task(
        get_luigi,
        cities
):
    expected_result = {
        'status': 'success',
        'data': cities
    }

    task = GetCitiesTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi()
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_result == json.loads(task_result)


@pytest.mark.parametrize(
    "cities_result, expected_result",
    [
        ([Exception("hand made"), Exception("hand made"), 'cities'],
         {
            'status': 'success',
            'data': 'cities'
        }),
        ([Exception("hand made"), Exception("hand made"), Exception("hand made")],
         {
            'status': 'error',
            'data': {
                'message': 'Error retrieving cities',
                'task_name': 'GetCitiesTask'
            }
        }),
    ],
)
def test_get_cities_task_with_retries(
        mocker,
        cities_result,
        expected_result,
        get_luigi,
        retry_config,
        cities
):
    get_cities_mock = mocker.patch(
        'luigi_demo.tasks.get_cities_task.get_cities',
        side_effect=cities_result
    )

    task = GetCitiesTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi(retry_config)
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_result == json.loads(task_result)
    assert get_cities_mock.call_count == len(cities_result)
