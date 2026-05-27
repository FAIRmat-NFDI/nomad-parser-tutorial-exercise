from typing import (
    TYPE_CHECKING,
)

from nomad.metainfo.metainfo import Category

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import EntryData, EntryDataCategory, Section
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import Measurement
from nomad.metainfo import Quantity, SchemaPackage

m_package = SchemaPackage()


class ExampleCategory(EntryDataCategory):
    """
    A category for all measurements defined in the example nomad plugin.
    """

    m_def = Category(label='ExamplePlugin', categories=[EntryDataCategory])


class ExampleMicroscopyMeasurement(Measurement, EntryData):
    """
    Example microscopy measurement schema.
    """

    m_def = Section(
        categories=[ExampleCategory],
        label='Example Microscopy ELN',
    )

    file = Quantity(
        type=str,
        description='File containing the data.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    resolution = Quantity(
        type=float, description='Microscopy image resolution', shape=[2]
    )

    magnification = Quantity(
        type=float,
        description='Microscopy image magnification',
    )


m_package.__init_metainfo__()
