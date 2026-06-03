import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'schema_tutorial', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.settings.magnification == 5.0
    assert (
        entry_archive.data.results[0].image
        == '000spincoated_slide_after_annealing1-2500-0.jpeg'
    )


if __name__ == '__main__':
    test_schema_package()
