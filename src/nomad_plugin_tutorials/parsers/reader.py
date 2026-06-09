from typing import TYPE_CHECKING

from nomad.parsing.file_parser.mapping_parser import XMLParser
from nomad.utils import get_logger

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import BoundLogger


class ConcreteXMLParser(XMLParser):
    @property
    def logger(self):
        if not hasattr(self, '_logger') or self._logger is None:
            self._logger = get_logger(__name__)
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value


def parse_xml_file(filepath: str, logger: 'BoundLogger' = None) -> dict:
    return ConcreteXMLParser(filepath=filepath, logger=logger).to_dict()


def read_data_file(
    filepath: str, archive: 'EntryArchive', logger: 'BoundLogger'
) -> dict:
    """
    Reads the microscopy data file and converts it to a dictionary. Uses the `XMLParser`
    from NOMAD's parsing module. The file is accessed using the `archive.m_context`
    which provides a context for interacting with the raw files in current NOMAD upload.


    Args:
        filepath (str): The relative path to the microscopy data file in the current
            NOMAD upload.
        archive (EntryArchive): The NOMAD entry archive object.
        logger (BoundLogger): A bound logger object.

    Returns:
        dict: A dictionary containing the parsed microscopy data.
    """
    try:
        with archive.m_context.raw_file(filepath) as raw_file:
            data_dict = parse_xml_file(raw_file.name, logger).get('image_metadata', {})
        if not data_dict.get('@type') == 'microscopy':
            raise ValueError('Unexpected structure of the data file.')
    except Exception as e:
        logger.error(f'Failed to parse "{filepath}": {e}', exc_info=True)
        return {}
    return data_dict
