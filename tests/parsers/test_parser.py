import logging

from nomad.datamodel import EntryArchive

from nomad_parser_tutorial_exercise.exercise_3.parsers.parser import (
    ExampleMicroscopyParser,
)


def test_parse_file():
    parser = ExampleMicroscopyParser()
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging.getLogger()) # type: ignore

    assert archive.workflow2.name == 'test'
