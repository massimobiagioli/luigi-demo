from typing import List

import luigi
import pytest


@pytest.fixture
def get_luigi():
    def _build_luigi_conf(config: List[dict] = []):
        """
        config is a list on configurations dictionaries in the form:
            {
                "section":"name-of-the-section",
                "option":"name-of-the-option-of-the-section",
                "value":"string-value-of-the-option"
            }
        """
        conf = luigi.configuration.get_config()
        for cfg in config:
            conf.set(**cfg)
        return luigi

    return _build_luigi_conf
