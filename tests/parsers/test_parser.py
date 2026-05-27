import logging

from nomad.datamodel import EntryArchive

from nomad_parser_tutorial_exercise.exercise_2.parsers.parser import ExampleXMLParser


def test_parse_file():
    parser = ExampleXMLParser()
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging.getLogger()) # type: ignore

    assert archive.workflow2.name == 'test'
