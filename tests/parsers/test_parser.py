import logging
import math

from nomad.datamodel import EntryArchive

from nomad_plugin_tutorials.parsers.tutorial_3.parsers.parser import (
    ExampleMicroscopyParser,
)


def test_parse_file():
    parser = ExampleMicroscopyParser()
    archive = EntryArchive()
    parser.parse('tests/data/parsers/example.xml', archive, logging.getLogger())

    assert math.isclose(archive.data.magnification, 5.0, rel_tol=1e-9)


if __name__ == '__main__':
    test_parse_file()
