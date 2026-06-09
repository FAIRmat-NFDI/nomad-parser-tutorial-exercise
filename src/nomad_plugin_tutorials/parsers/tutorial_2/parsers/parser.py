from typing import (
    TYPE_CHECKING,
)

from nomad_plugin_tutorials.parsers.utils import create_archive

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.parsing.parser import MatchingParser

from nomad_plugin_tutorials.parsers.tutorial_2.schema.schema_package import (
    ExampleMicroscopyMeasurement,
    RawFileData,
)


class ExampleXMLParser(MatchingParser):
    """
    Parser for matching .xml metadata files and creating instances of IFMModel.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
    ) -> None:
        filename = mainfile.rsplit('/', maxsplit=1)[-1]
        name = filename.split('.')[0]
        logger.info(f' Example XML Parser called {filename}')

        measurement_entry = ExampleMicroscopyMeasurement(
            metadata_file=filename,
        )

        archive.data = RawFileData(
            measurement=create_archive(
                measurement_entry, archive, f'{name}.archive.json'
            )
        )
        archive.metadata.entry_name = f'{name} data file'
