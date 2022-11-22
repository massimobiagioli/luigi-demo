import json
import uuid

import pytest
from luigi.mock import MockTarget

from luigi_demo.models.weather_forecast import WeatherForecast
from luigi_demo.tasks.get_weather_data_task import GetWeatherDataTask


def test_get_weather_data_task(get_luigi, weather_data, mocker):
    mocker.patch(
        "luigi_demo.tasks.get_weather_data_task.get_weather_data",
        return_value=weather_data,
    )

    task = GetWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi()
    luigi.build([task], local_scheduler=True)

    task_result = MockTarget.fs.get_data(task.output_name)
    task_result_data = json.loads(task_result)

    assert weather_data == [WeatherForecast(**d) for d in task_result_data]


@pytest.mark.parametrize(
    "weather_data_result, expected_result",
    [
        ([Exception("hand made"), "weather_data"], "weather_data"),
        (
            [Exception("hand made"), Exception("hand made"), "weather_data"],
            "weather_data",
        ),
        (
            [Exception("hand made"), Exception("hand made"), Exception("hand made")],
            "no_result",
        ),
    ],
)
def test_get_weather_data_task_with_retries(
    request, mocker, weather_data_result, expected_result, get_luigi, retry_config
):
    expected_result = request.getfixturevalue(expected_result)
    weather_data_result = [
        r for r in weather_data_result if isinstance(r, Exception)
    ] + [request.getfixturevalue(r) for r in weather_data_result if isinstance(r, str)]

    get_weather_data_mock = mocker.patch(
        "luigi_demo.tasks.get_weather_data_task.get_weather_data",
        side_effect=weather_data_result,
    )

    task = GetWeatherDataTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi(retry_config)
    luigi.build([task], local_scheduler=True)

    if expected_result is None:
        with pytest.raises(Exception):
            MockTarget.fs.get_data(task.output_name)
    else:
        task_result = MockTarget.fs.get_data(task.output_name)
        task_result_data = json.loads(task_result)

        assert expected_result == [WeatherForecast(**d) for d in task_result_data]
        assert get_weather_data_mock.call_count == len(weather_data_result)
