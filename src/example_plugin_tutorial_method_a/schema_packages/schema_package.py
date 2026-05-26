from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    InstrumentReference,
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
        from example_plugin_tutorial_method_a.util.reader import read_xml_to_dict

        super().normalize(archive, logger)

        if self.file is not None:
            data_dict_full = read_xml_to_dict(self.file, archive, logger) # type: ignore
            data_dict = data_dict_full.get('image_metadata', {})
            if not (isinstance(data_dict, dict) and data_dict.get('@type') == 'microscopy'):
                logger.warning('Unexpected structure of the xml file')
                return

            if 'resolution' in data_dict:
                self.resolution = [float(x) for x in data_dict['resolution'].split('x')]
            if 'magnification' in data_dict:
                self.magnification = float(data_dict['magnification'][:-1])
            if 'sample' in data_dict and isinstance(data_dict['sample'], dict) and 'sample_ID' in data_dict['sample']:
                sample = data_dict['sample']
                self.samples = [
                    CompositeSystemReference(
                        lab_id=sample['sample_ID'],
                    )
                ]
            if 'deviceName' in data_dict:
                self.instruments = [
                    InstrumentReference(
                        name=data_dict['deviceName'],
                    )
                ]
            if 'datetime' in data_dict:
                self.datetime = data_dict['datetime']


m_package.__init_metainfo__()
