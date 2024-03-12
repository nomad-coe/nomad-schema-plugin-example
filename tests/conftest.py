import glob
import json
import os

import pytest
from nomad.utils import structlogging


@pytest.fixture(scope='function')
def capture_error_from_logger(caplog):
    """
    Extracts log messages from the logger and raises an assertion error if any
    ERROR messages are found.
    """
    caplog.handler.formatter = structlogging.ConsoleFormatter()
    yield caplog
    for record in caplog.get_records(when='call'):
        if record.levelname in ['ERROR']:
            try:
                msg = structlogging.ConsoleFormatter.serialize(json.loads(record.msg))
            except Exception:
                msg = record.msg
            assert False, msg


@pytest.fixture(scope='function')
def clean_up():
    """
    Deletes all files created during the test.
    """
    yield
    # add file extensions as wildcard for clean up
    file_types = ['*.ipynb']
    generated_files = []
    for file_type in file_types:
        generated_files = glob.glob(
            os.path.join(os.path.dirname(__file__), 'data', file_type)
        )
    for file in generated_files:
        os.remove(file)
