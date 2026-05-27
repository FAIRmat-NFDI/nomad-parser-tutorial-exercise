from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category


class ExampleCategory(EntryDataCategory):
    """
    A category for all measurements defined in the example nomad plugin.
    """

    m_def = Category(label='ExamplePlugin', categories=[EntryDataCategory])


class ExampleMicroscopySchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_parser_tutorial_exercise.exercise_2.schema_packages.schema_package import (
            m_package,
        )

        return m_package


example_microscopy_schema_entry_point = ExampleMicroscopySchemaEntryPoint(
    name='ExampleMicroscopy',
    description='Example microscopy schema package entry point.',
)
