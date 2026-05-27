from nomad.config.models.plugins import ParserEntryPoint


class ExampleMicroscopyParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_parser_tutorial_exercise.exercise_2.parsers.parser import (
            ExampleXMLParser,
        )

        return ExampleXMLParser(**self.model_dump())


example_microscopy_parser_entry_point = ExampleMicroscopyParserEntryPoint(
    name='ExampleMicroscopyParser',
    description='Example microscopy parser entry point.',
    mainfile_name_re=r'.*\.xml$',
)
