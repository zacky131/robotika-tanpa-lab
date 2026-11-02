"""Uji gaya kode (flake8) — dijalankan oleh `colcon test`."""
from ament_flake8.main import main_with_errors
import pytest


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8():
    rc, errors = main_with_errors(argv=[])
    assert rc == 0, \
        'Ditemukan %d pelanggaran gaya kode:\n' % len(errors) + '\n'.join(errors)
