from typing import TYPE_CHECKING

from nomad.parsing.file_parser.mapping_parser import XMLParser

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import BoundLogger


def read_xml_to_dict(file: str, archive: 'EntryArchive', logger: 'BoundLogger') -> dict:
    try:
        with archive.m_context.raw_file(file) as raw_file:
            result = XMLParser(filepath=raw_file.name).to_dict()
    except Exception as e:
        logger.error(f'Failed to parse xml file: {e}')
        result = {}

    return result
