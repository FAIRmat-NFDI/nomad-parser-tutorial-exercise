from nomad.config.models.plugins import ParserEntryPoint


class MicroscopyParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.parsers.tutorial_2.parsers.parser import (
            OpticalMicroscopyParser,
        )

        return OpticalMicroscopyParser(**self.model_dump())


microscopy = MicroscopyParserEntryPoint(
    name='Parser Tutorial 2: Microscopy Parser',
    description='Microscopy parser entry point.',
    mainfile_name_re=r'.*\.xml$',
)
