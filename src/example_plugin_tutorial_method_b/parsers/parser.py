from typing import (
    TYPE_CHECKING,
)

from util.utils import create_archive

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.parsing.parser import MatchingParser

from example_plugin_tutorial_method_b.schema_packages.schema_package import (
    ExampleMicroscopyMeasurement,
    RawFileData,
)

configuration = config.get_plugin_entry_point(
    'example_plugin_tutorial.parsers:example_microscopy_parser_entry_point'
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
        # logger.info('ExampleXMLParser.parse')
        # data_file = mainfile.rsplit('/', maxsplit=1)[-1]
        filename = mainfile.rsplit('/', maxsplit=1)[-1]
        name = filename.split('.')[0]
        logger.info(f' Example XML Parser called {filename}')

        catalytic_reaction = ExampleMicroscopyMeasurement(
            data_file=filename,
        )

        archive.data = RawFileData(
            measurement=create_archive(
                catalytic_reaction, archive, f'{name}.archive.json'
            )
        )
        archive.metadata.entry_name = f'{name} data file'

        # file_name = f'{data_file[:-2]}archive.json'
        # archive.metadata.entry_type = 'RawMetadataFile'
        # new_empty_entry = IFMModel.m_from_dict(IFMModel.m_def.a_template)
        # new_empty_entry.method = 'IFM Model'

        # reprocessing_needed = False

        # with archive.m_context.update_entry(
        #     file_name, write=True, process=False
        # ) as model_entry:
        #     if (
        #         model_entry.get('data') is None
        #         or model_entry['data'].get('method') != 'IFM Model'
        #     ):
        #         model_entry['data'] = new_empty_entry.m_to_dict(with_root_def=True)
        #         logger.info(f'IFMModel entry {file_name} created.')
        #         reprocessing_needed = True
        #     if model_entry['data'].get('file') is None:
        #         model_entry['data']['file'] = data_file
        #         reprocessing_needed = True

        # if reprocessing_needed:
        #     with archive.m_context.update_entry(
        #         file_name, write=True, process=True
        #     ) as model_entry:
        #         pass
