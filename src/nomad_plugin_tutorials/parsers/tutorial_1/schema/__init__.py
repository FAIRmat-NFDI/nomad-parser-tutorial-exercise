from nomad.config.models.plugins import SchemaPackageEntryPoint


class MicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.parsers.tutorial_1.schema.schema_package import (
            m_package,
        )

        return m_package


microscopy = MicroscopySchemaEntryPoint(
    name='Parser Tutorial 1: Microscopy Schema',
    description='Microscopy schema package entry point.',
)
