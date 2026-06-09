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
        filename = mainfile.rsplit('/', maxsplit=1)[-1]
        name = filename.split('.')[0]
        logger.info(f' Example XML Parser called {filename}')

        measurement_entry = OpticalMicroscopy(data_file=filename)

        archive.data = RawFileOpticalMicroscopy(
            measurement=create_archive(
                measurement_entry, archive, f'{name}.archive.json'
            )
        )
        archive.metadata.entry_name = f'{name} data file'
