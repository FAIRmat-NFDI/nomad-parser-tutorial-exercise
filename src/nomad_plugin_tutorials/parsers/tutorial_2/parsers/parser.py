from typing import TYPE_CHECKING

from nomad.parsing.parser import MatchingParser

from nomad_plugin_tutorials.parsers.tutorial_2.schema.schema_package import (
    OpticalMicroscopy,
    RawFileOpticalMicroscopy,
)
from nomad_plugin_tutorials.parsers.utils import create_archive

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive


class OpticalMicroscopyParser(MatchingParser):
    """
    Parser for matching the data files from Optical Microscopy and creating
    `RawFileOpticalMicroscopy` and `OpticalMicroscopy` ELN entries.

    `RawFileOpticalMicroscopy` is the main archive linked to the data file, whereas
    `OpticalMicroscopy` ELN is an additional entry linked to an `{name}.archive.json`
    file.
    """

    def parse(
        self, mainfile: str, archive: 'EntryArchive', logger=None, child_archives=None
    ) -> None:
        data_file = mainfile.rsplit('/raw/', maxsplit=1)[-1]
        logger.info(f' Example XML Parser called {data_file}')

        measurement = OpticalMicroscopy(data_file=data_file)
        measurement_entry_archive = create_archive(
            measurement, archive, data_file.replace('.xml', '.archive.json')
        )

        archive.data = RawFileOpticalMicroscopy(measurement=measurement_entry_archive)
