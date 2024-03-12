import os.path

from nomad.client import normalize_all, parse


def test_schema(capture_error_from_logger, clean_up):
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.analysis_type == 'Generic'
    # TODO: Add tests for generated jupyter notebook
