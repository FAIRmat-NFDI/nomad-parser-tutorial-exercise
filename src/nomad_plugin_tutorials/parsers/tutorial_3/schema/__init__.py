from nomad.config.models.plugins import SchemaPackageEntryPoint


class MicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.parsers.tutorial_3.schema.schema_package import (
            m_package,
        )

        return m_package


microscopy = MicroscopySchemaEntryPoint(
    name='Parser Tutorial 3: Microscopy Schema',
    description='Microscopy schema package entry point.',
)
