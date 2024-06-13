from nomad.datamodel import EntryArchive

from nomad_batteries import ExampleSection

from . import LOGGER


def test_dummy():
    schema = ExampleSection(name='World')
    schema.normalize(EntryArchive(), LOGGER)
    assert schema.message == 'Hello World!'
