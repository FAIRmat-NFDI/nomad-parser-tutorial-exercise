from nomad.config.models.plugins import SchemaPackageEntryPoint


class ExampleMicroscopyEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_parser_tutorial_exercise.exercise_3.schema_packages.schema_package import (
            m_package,
        )

        return m_package


example_microscopy_entry_point = ExampleMicroscopyEntryPoint(
    name='ExampleMicroscopy',
    description='Example microscopy schema package entry point.',
)
