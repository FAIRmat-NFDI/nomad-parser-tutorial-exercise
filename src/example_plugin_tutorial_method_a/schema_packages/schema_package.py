from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.metainfo.eln import ELNMeasurement

from example_plugin_tutorial_method_a.schema_packages import ExampleCategory

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage, Section

configuration = config.get_plugin_entry_point(
    'example_plugin_tutorial_method_a.schema_packages:example_microscopy_entry_point'
)

m_package = SchemaPackage()


class ExampleMicroscopyMeasurement(ELNMeasurement):
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
        type=float,
        description='Microscopy image resolution',
        shape=[2]
    )

    magnification = Quantity(
        type=float,
        description='Microscopy image magnification',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


m_package.__init_metainfo__()
