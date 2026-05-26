from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category
from pydantic import Field


class ExampleCategory(EntryDataCategory):
    """
    A category for all measurements defined in the example nomad plugin.
    """

    m_def = Category(label='ExamplePlugin', categories=[EntryDataCategory])


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from example_plugin_tutorial_method_b.schema_packages.schema_package import (
            m_package,
        )

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
)
