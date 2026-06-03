"""
This module defines the entry point for the microscopy schema package. The entry point
contains configuration, but also a resource, which lives in a separate Python module.
This split enables lazy-loading: the configuration can be loaded immediately, while the
resource (schema package) is loaded later when/if it is required.

Read further in the NOMAD documentation: https://nomad-lab.eu/prod/v1/docs/
"""

from nomad.config.models.plugins import SchemaPackageEntryPoint


class MicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_parser_tutorial_exercise.schema_tutorial.schema_package import (
            m_package,
        )

        return m_package


microscopy_schema_entry_point = MicroscopySchemaEntryPoint(
    name='Microscopy Schema',
    description='Example microscopy schema package entry point.',
)
