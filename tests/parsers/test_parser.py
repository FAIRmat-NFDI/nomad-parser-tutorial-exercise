import math

from nomad.client import parse


def test_parse_file():
    archive = parse('tests/data/parsers/example.xml')[0]

    assert math.isclose(archive.data.magnification, 5.0, rel_tol=1e-9)


if __name__ == '__main__':
    test_parse_file()
