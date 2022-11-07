import json
import uuid

from luigi.mock import MockTarget

from luigi_demo.tasks.get_cities_task import GetCitiesTask


def test_get_cities_task(get_luigi):
    expected_cities = [
        'Milano',
        'Torino',
        'Roma',
        'Napoli',
        'Palermo',
    ]

    task = GetCitiesTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi()
    luigi.build([task], local_scheduler=True)

    data = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_cities == json.loads(data)


def test_get_cities_task_with_retry(mocker, get_luigi):
    expected_cities = [
        'Milano',
        'Torino',
        'Roma',
        'Napoli',
        'Palermo',
    ]

    get_cities_mock = mocker.patch(
        'luigi_demo.tasks.get_cities_task.get_cities',
        side_effect=[
            Exception("hand made"),
            Exception("hand made"),
            expected_cities
        ]
    )

    task = GetCitiesTask(debug=True, nonce=str(uuid.uuid4()))
    luigi = get_luigi(
        [
            {
                "section": 'worker',
                "option": 'keep_alive',
                "value": 'True'
            },
            {
                "section": 'scheduler',
                "option": 'retry_delay',
                "value": '1'
            }
        ]
    )
    luigi.build([task], local_scheduler=True)

    data = MockTarget.fs.get_data(task.debug_output_name)

    assert expected_cities == json.loads(data)
    assert get_cities_mock.call_count == 3
