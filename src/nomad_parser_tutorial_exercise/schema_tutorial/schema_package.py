import os
from typing import TYPE_CHECKING

from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import (
    BrowserAdaptors,
    BrowserAnnotation,
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    InstrumentReference,
    Measurement,
)
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from nomad_parser_tutorial_exercise.util.reader import read_data_file
from nomad_parser_tutorial_exercise.util.utils import merge_sections

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = SchemaPackage()


class OpticalMicroscopySettings(ArchiveSection):
    """
    An example schema for optical microscopy measurement settings.
    """

    resolution = Quantity(
        type=float, description='Microscopy image resolution', shape=[2]
    )
    magnification = Quantity(
        type=float,
        description='Microscopy image magnification',
    )


class OpticalMicroscopyResults(ArchiveSection):
    """
    An example schema for optical microscopy measurement results.
    """

    image = Quantity(
        type=str,
        description='Microscopy image file.',
        a_browser=BrowserAnnotation(adaptor=BrowserAdaptors.RawFileAdaptor),
    )


class OpticalMicroscopy(Measurement):
    """
    An example schema for optical microscopy measurements.
    """

    m_def = Section(
        label='Example Microscopy ELN',
    )

    settings = SubSection(
        section_def=OpticalMicroscopySettings,
        description='Microscopy settings.',
    )
    results = SubSection(
        section_def=OpticalMicroscopyResults,
        description='Microscopy results.',
        repeats=True,
    )


class OpticalMicroscopyELN(OpticalMicroscopy, EntryData):
    """
    An example ELN schema for optical microscopy measurements. Using `EntryData` as
    a parent section enables this section to be used for creating NOMAD entries.
    """

    data_file = Quantity(
        type=str,
        description='Data file coming from the microscope.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    def write_data(self, data_dict: dict, logger: 'BoundLogger') -> None:
        """
        Writes the data from the provided dictionary to the quantities of the schema.
        Uses the `merge_sections` utility function.

        Args:
            data_dict (dict): A dictionary containing the data to be written.
            logger (BoundLogger): A structlog logger.
        """
        measurement = OpticalMicroscopy()
        if datetime := data_dict.get('datetime'):
            measurement.datetime = datetime

        measurement.m_setdefault('settings')
        if resolution := data_dict.get('resolution'):
            measurement.settings.resolution = [float(x) for x in resolution.split('x')]
        if magnification := data_dict.get('magnification'):
            measurement.settings.magnification = float(magnification[:-1])

        measurement.m_setdefault('results/0')
        if image_file_name := data_dict.get('imageFileName'):
            measurement.results[0].image = os.path.join(
                os.path.dirname(self.data_file), image_file_name
            )

        if (
            'sample' in data_dict
            and isinstance(data_dict['sample'], dict)
            and 'sample_ID' in data_dict['sample']
        ):
            sample = data_dict['sample']
            self.samples = [
                CompositeSystemReference(
                    lab_id=sample['sample_ID'],
                )
            ]
        if device_name := data_dict.get('deviceName'):
            self.instruments = [InstrumentReference(name=device_name)]

        merge_sections(self, measurement, logger=logger)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        Redefining the `normalize` method to read the data from the provided file and
        populate other quantities of the schema. This method is called when the entry
        is processed.
        """

        super().normalize(archive, logger)

        data_dict = {}
        if self.data_file is not None:
            data_dict = read_data_file(self.data_file, archive, logger)
        if data_dict:
            self.write_data(data_dict, logger)


m_package.__init_metainfo__()
