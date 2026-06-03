from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    InstrumentReference,
    Measurement,
)
from nomad.datamodel.metainfo.eln import ELNMeasurement
from nomad.metainfo.metainfo import Category

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.data import EntryDataCategory, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage, Section

from nomad_parser_tutorial_exercise.util.utils import merge_sections

m_package = SchemaPackage()


class ExampleCategory(EntryDataCategory):
    """
    A category for all measurements defined in the example nomad plugin.
    """

    m_def = Category(label='ExamplePlugin', categories=[EntryDataCategory])


class RawFileData(Schema):
    """
    Section for storing a directly parsed raw data file.
    """

    m_def = Section(
        description='A section for storing the raw data file that was parsed'
        'by the example parser.',
    )
    measurement = Quantity(
        type=Measurement,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            description='A reference to the measurement entry that was generated from '
            'this data.',
        ),
    )


class ExampleMicroscopyMeasurement(ELNMeasurement):
    """
    Example microscopy measurement schema.
    """

    m_def = Section(
        categories=[ExampleCategory],
        label='Example Microscopy ELN',
    )

    metadata_file = Quantity(
        type=str,
        description='File containing the data.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    image_file = Quantity(
        type=str,
        description='Microscopy image file.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    resolution = Quantity(
        type=float, description='Microscopy image resolution', shape=[2]
    )

    magnification = Quantity(
        type=float,
        description='Microscopy image magnification',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        from nomad_parser_tutorial_exercise.util.reader import (
            read_data_file,
        )

        if self.metadata_file is not None:
            data_dict_full = read_data_file(self.metadata_file, archive, logger)  # type: ignore
            data_dict = data_dict_full.get('image_metadata', {})
            if not (
                isinstance(data_dict, dict) and data_dict.get('@type') == 'microscopy'
            ):
                logger.warning('Unexpected structure of the xml file')
                return

            update_section = ExampleMicroscopyMeasurement()
            if 'resolution' in data_dict:
                update_section.resolution = [
                    float(x) for x in data_dict['resolution'].split('x')
                ]
            if 'magnification' in data_dict:
                update_section.magnification = float(data_dict['magnification'][:-1])
            if (
                'sample' in data_dict
                and isinstance(data_dict['sample'], dict)
                and 'sample_ID' in data_dict['sample']
            ):
                sample = data_dict['sample']
                update_section.samples = [
                    CompositeSystemReference(
                        lab_id=sample['sample_ID'],
                    )
                ]
            if 'deviceName' in data_dict:
                update_section.instruments = [
                    InstrumentReference(
                        name=data_dict['deviceName'],
                    )
                ]
            if 'datetime' in data_dict:
                update_section.datetime = data_dict['datetime']
            if 'imageFileName' in data_dict:
                update_section.image_file = data_dict['imageFileName']
            merge_sections(self, update_section, logger)  # pyright: ignore[reportArgumentType]

        super().normalize(archive, logger)


m_package.__init_metainfo__()
