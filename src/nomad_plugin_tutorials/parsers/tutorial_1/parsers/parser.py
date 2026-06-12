import os
from typing import (
    TYPE_CHECKING,
)

from nomad.parsing.parser import MatchingParser

from nomad_plugin_tutorials.parsers.reader import read_data_file
from nomad_plugin_tutorials.parsers.tutorial_1.schema.schema_package import (
    OpticalMicroscopy,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive


class OpticalMicroscopyParser(MatchingParser):
    def parse(
        self, mainfile: str, archive: 'EntryArchive', logger=None, child_archives=None
    ) -> None:
        data_file_path = mainfile.rsplit('/raw/', maxsplit=1)[-1]
        data_dict = read_data_file(data_file_path, archive, logger)

        measurement = OpticalMicroscopy(data_file=data_file_path)
        if datetime := data_dict.get('datetime'):
            measurement.datetime = datetime
        if (
            'sample' in data_dict
            and isinstance(data_dict['sample'], dict)
            and 'sample_ID' in data_dict['sample']
        ):
            measurement.m_setdefault('samples/0')
            measurement.samples[0].lab_id = data_dict['sample']['sample_ID']
            if 'description' in data_dict['sample']:
                measurement.description = data_dict['sample']['description']

        measurement.m_setdefault('settings')
        if resolution := data_dict.get('resolution'):
            measurement.settings.resolution = [float(x) for x in resolution.split('x')]
        if magnification := data_dict.get('magnification'):
            measurement.settings.magnification = float(magnification[:-1])

        measurement.m_setdefault('results/0')
        if image_file_name := data_dict.get('imageFileName'):
            measurement.results[0].image = os.path.join(
                os.path.dirname(data_file_path), image_file_name
            )

        archive.data = measurement
