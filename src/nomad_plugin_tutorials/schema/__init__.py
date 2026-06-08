"""
This module defines the entry point for the microscopy schema package. The entry point
contains configuration, but also a resource, which lives in a separate Python module.
This split enables lazy-loading: the configuration can be loaded immediately, while the
resource (schema package) is loaded later when/if it is required.

Read further in the NOMAD documentation: https://nomad-lab.eu/prod/v1/docs/
"""

from nomad.config.models.plugins import SchemaPackageEntryPoint


class BlackbodyRadiationSchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_tutorials.schema.schema_package import (
            m_package,
        )

        return m_package


blackbody_radiation = BlackbodyRadiationSchemaEntryPoint(
    name="Blackbody Radiation Schema",
    description="Example blackbody radiation schema package entry point.",
)
