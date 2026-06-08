from nomad.config.models.plugins import SchemaPackageEntryPoint


class ExampleMicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.parsers.tutorial_2.schema_packages.schema_package import (
            m_package,
        )

        return m_package


example_microscopy_schema_entry_point = ExampleMicroscopySchemaEntryPoint(
    name='ExampleMicroscopy',
    description='Example microscopy schema package entry point.',
)
