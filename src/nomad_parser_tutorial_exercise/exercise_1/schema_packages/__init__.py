from nomad.config.models.plugins import SchemaPackageEntryPoint


class ExampleMicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_parser_tutorial_exercise.exercise_1.schema_packages.schema_package import (
            m_package,
        )

        return m_package


example_microscopy_schema_entry_point = ExampleMicroscopySchemaEntryPoint(
    name='ExampleMicroscopy',
    description='Example microscopy schema package entry point.',
)
