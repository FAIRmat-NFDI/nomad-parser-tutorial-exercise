from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from nomad.datamodel.data import (
        ArchiveSection,
    )
    from structlog import BoundLogger


def _not_equal(a, b) -> bool:
    try:
        comparison = a != b
    except ValueError:
        # If the comparison fails, we assume they are not equal
        return True
    if isinstance(comparison, np.ndarray):
        return comparison.any()  # pyright: ignore[reportReturnType]
    return comparison


def merge_sections(  # noqa: PLR0912
    section: 'ArchiveSection',
    update: 'ArchiveSection',
    logger: 'BoundLogger' = None,  # pyright: ignore[reportArgumentType]
) -> None:
    """
    Unpopulated quantities and subsections in the `section` will be populated with the
    values from the `update` section.
    If a quantity is present in both sections but with different values, no change is
    made.
    If a repeating subsection is present in both sections, and they are of the same
    length, the subsections will be merged recursively. Else, no change is made.

    Args:
        section (ArchiveSection): section to update.
        update (ArchiveSection): section to update from.
        logger (BoundLogger, optional): A structlog logger.
    """
    if update is None:
        return
    if section is None:
        section = update.m_copy()
        return
    if not isinstance(section, type(update)):
        raise TypeError(
            'Cannot merge sections of different types: '
            f'{type(section)} and {type(update)}'
        )
    for name, quantity in update.m_def.all_quantities.items():  # type: ignore
        if not update.m_is_set(quantity):
            continue
        if not section.m_is_set(quantity):
            section.m_set(quantity, update.m_get(quantity))
        elif _not_equal(section.m_get(quantity), update.m_get(quantity)):
            warning = f'Merging sections with different values for quantity "{name}".'
            if logger:
                logger.warning(warning)
            else:
                print(warning)
    for name, sub_section_def in update.m_def.all_sub_sections.items():  # type: ignore
        count = section.m_sub_section_count(sub_section_def)
        if count == 0:
            for update_sub_section in update.m_get_sub_sections(sub_section_def):
                section.m_add_sub_section(sub_section_def, update_sub_section)
        elif count == update.m_sub_section_count(sub_section_def):
            for i in range(count):
                merge_sections(
                    section.m_get_sub_section(sub_section_def, i),  # pyright: ignore[reportArgumentType]
                    update.m_get_sub_section(sub_section_def, i),  # pyright: ignore[reportArgumentType]
                    logger,
                )
        elif update.m_sub_section_count(sub_section_def) > 0:
            warning = (
                f'Merging sections with different number of "{name}" sub sections.'
            )
            if logger:
                logger.warning(warning)
            else:
                print(warning)
