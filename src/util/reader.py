import os
from typing import TYPE_CHECKING

from nomad.parsing.file_parser.mapping_parser import XMLParser

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import BoundLogger

def read_xml_to_dict(file: str, archive: 'EntryArchive', logger: 'BoundLogger') -> dict:
    try:
        upload_id=archive.metadata.upload_id
        filepath = os.path.join(
            os.getcwd(),
            f'.volumes/fs/staging/{upload_id[0:2]}/{upload_id}/raw', # type: ignore
            file
        )
        result = XMLParser(filepath=filepath).to_dict()
    except Exception as e:
        logger.error(f'Failed to parse xml file: {e}')
        result = {}

    return result
