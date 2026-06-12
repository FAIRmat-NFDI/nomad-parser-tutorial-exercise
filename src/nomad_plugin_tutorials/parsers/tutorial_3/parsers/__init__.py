from nomad.config.models.plugins import ElnParserEntryPoint

microscopy = ElnParserEntryPoint(
    name='Parser Tutorial 3: Microscopy Parser',
    description='Microscopy parser entry point.',
    mainfile_name_re=r'.*\.xml$',
    eln_m_def='nomad_plugin_tutorials.parsers.tutorial_3.schema.schema_package.'
    'OpticalMicroscopy',
)
