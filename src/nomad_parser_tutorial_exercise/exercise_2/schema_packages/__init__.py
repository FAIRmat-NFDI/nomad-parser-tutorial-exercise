from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category
from pydantic import Field


class ExampleCategory(EntryDataCategory):
    """
    A category for all measurements defined in the example nomad plugin.
    """

    m_def = Category(label='ExamplePlugin', categories=[EntryDataCategory])


class ExampleMicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_parser_tutorial_exercise.exercise_2.schema_packages.schema_package import (
            m_package,
        )

        return m_package


example_microscopy_schema_entry_point = ExampleMicroscopySchemaEntryPoint(
    name='ExampleMicroscopy',
    description='Example microscopy schema package entry point.',
)
