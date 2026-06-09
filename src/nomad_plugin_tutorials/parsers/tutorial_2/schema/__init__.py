from nomad.config.models.plugins import SchemaPackageEntryPoint


class MicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.parsers.tutorial_2.schema.schema_package import (
            m_package,
        )

        return m_package


microscopy = MicroscopySchemaEntryPoint(
    name='Parser Tutorial 2: Microscopy Schema',
    description='Microscopy schema package entry point.',
)
