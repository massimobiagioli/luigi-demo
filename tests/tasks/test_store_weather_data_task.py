import json
import uuid

import pytest
from luigi.mock import MockTarget

from luigi_demo.tasks.store_weather_data_task import StoreWeatherDataTask


def test_store_weather_data_task(get_luigi, mocker):
    mocker.patch(
        "luigi_demo.tasks.store_weather_data_task.store_weather_data", return_value=None
    )

    expected_result = {"processed": 5}

    task = StoreWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi()
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.output_name)

    assert expected_result == json.loads(task_result)


@pytest.mark.parametrize(
    "store_weather_data_result, expected_result",
    [
        ([Exception("hand made"), None], {"processed": 5}),
        ([Exception("hand made"), Exception("hand made"), None], {"processed": 5}),
        (
            [Exception("hand made"), Exception("hand made"), Exception("hand made")],
            None,
        ),
    ],
)
def test_get_weather_data_task_with_retries(
    mocker, store_weather_data_result, expected_result, get_luigi, retry_config
):
    store_weather_data_mock = mocker.patch(
        "luigi_demo.tasks.store_weather_data_task.store_weather_data",
        side_effect=store_weather_data_result,
    )

    task = StoreWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi(retry_config)
    luigi.build([task], local_scheduler=True)

    if expected_result is None:
        with pytest.raises(Exception):
            MockTarget.fs.get_data(task.output_name)
    else:
        task_result = MockTarget.fs.get_data(task.output_name)

        assert expected_result == json.loads(task_result)
        assert store_weather_data_mock.call_count == len(store_weather_data_result)
