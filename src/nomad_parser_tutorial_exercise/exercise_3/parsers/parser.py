from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.metainfo.basesections.v1 import (
    CompositeSystemReference,
    InstrumentReference,
)
from nomad.parsing.file_parser.mapping_parser import XMLParser
from nomad.parsing.parser import MatchingParser

from nomad_parser_tutorial_exercise.exercise_3.schema_packages.schema_package import (
    ExampleMicroscopyMeasurement,
)


class ExampleMicroscopyParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger' = None,  # pyright: ignore[reportArgumentType]
        child_archives: dict[str, 'EntryArchive'] = None,  # pyright: ignore[reportArgumentType]
    ) -> None:
        data_dict_full = XMLParser(filepath=mainfile).to_dict()
        data_dict = data_dict_full.get('image_metadata', {})

        entry_data_section = ExampleMicroscopyMeasurement(
            metadata_file=mainfile.rsplit('/raw/', maxsplit=1)[-1]
        )
        if not (isinstance(data_dict, dict) and data_dict.get('@type') == 'microscopy'):
            logger.warning('Unexpected structure of the xml file')
            return

        if 'resolution' in data_dict:
            entry_data_section.resolution = [
                float(x) for x in data_dict['resolution'].split('x')
            ]
        if 'magnification' in data_dict:
            entry_data_section.magnification = float(data_dict['magnification'][:-1])
        if (
            'sample' in data_dict
            and isinstance(data_dict['sample'], dict)
            and 'sample_ID' in data_dict['sample']
        ):
            sample = data_dict['sample']
            entry_data_section.samples = [
                CompositeSystemReference(
                    lab_id=sample['sample_ID'],
                )
            ]
        if 'deviceName' in data_dict:
            entry_data_section.instruments = [
                InstrumentReference(
                    name=data_dict['deviceName'],
                )
            ]
        if 'datetime' in data_dict:
            entry_data_section.datetime = data_dict['datetime']
        if 'imageFileName' in data_dict:
            entry_data_section.image_file = data_dict['imageFileName']

        archive.data = entry_data_section
