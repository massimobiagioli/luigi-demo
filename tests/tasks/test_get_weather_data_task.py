import json
import uuid

import pytest
from luigi.mock import MockTarget

from luigi_demo.tasks.get_weather_data_task import GetWeatherDataTask


def test_get_weather_task(
        get_luigi,
        weather_data,
        mocker
):
    mocker.patch(
        'luigi_demo.tasks.get_weather_data_task.get_weather_data',
        return_value=weather_data
    )

    expected_result = {
        'status': 'success',
        'data': weather_data
    }

    task = GetWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi()
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_result == json.loads(task_result)


@pytest.mark.parametrize(
    "weather_data_result, expected_result",
    [
        ([Exception("hand made"), Exception("hand made"), 'weather_data'],
         {
            'status': 'success',
            'data': 'weather_data'
        }),
        ([Exception("hand made"), Exception("hand made"), Exception("hand made")],
         {
            'status': 'error',
            'data': {
                'message': 'Error retrieving weather data',
                'task_name': 'GetWeatherDataTask'
            }
        }),
    ],
)
def test_get_weather_data_task_with_retries(
        mocker,
        weather_data_result,
        expected_result,
        get_luigi,
        retry_config,
        weather_data
):
    get_weather_data_mock = mocker.patch(
        'luigi_demo.tasks.get_weather_data_task.get_weather_data',
        side_effect=weather_data_result
    )

    task = GetWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi(retry_config)
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_result == json.loads(task_result)
    assert get_weather_data_mock.call_count == len(weather_data_result)
