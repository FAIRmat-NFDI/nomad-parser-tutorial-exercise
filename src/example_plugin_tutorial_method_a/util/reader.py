import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING, TextIO

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

def read_xml_to_dict(file_obj: TextIO, archive: 'EntryArchive', logger: 'BoundLogger') -> dict:
    tree = ET.parse(file_obj)
    root = tree.getroot()

    if root.attrib.get("type") != "microscopy":
        logger.warn('The file is not a microscopy xml file.')
        return {}

    #TODO add reader here

    return {}
