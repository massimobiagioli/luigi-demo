import luigi
import pytest


@pytest.fixture
def get_luigi():
    def _build_luigi_conf(config=None):
        """
        config is a list on configurations dictionaries in the form:
            {
                "section":"name-of-the-section",
                "option":"name-of-the-option-of-the-section",
                "value":"string-value-of-the-option"
            }
        """
        if config is None:
            config = []
        conf = luigi.configuration.get_config()
        for cfg in config:
            conf.set(**cfg)
        return luigi

    return _build_luigi_conf


@pytest.fixture
def retry_config():
    return [
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


@pytest.fixture
def cities():
    return ['Milano', 'Torino', 'Roma', 'Napoli', 'Palermo']
