from pathlib import Path

import pytest

import concat_ac3

#Authors: benxyzzy


@pytest.fixture()
def stg_filepath():
    return Path("./958401-test.stg").resolve()


def test_concat_ac3(stg_filepath, monkeypatch):
    """High-level "smoke test" to check it runs without errors."""
    FG_ROOT = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/"
    monkeypatch.setenv("FG_ROOT", FG_ROOT)
    monkeypatch.setattr("concat_ac3.FG_ROOT", FG_ROOT)

    FG_SCENERY = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/Scenery/SceneryPack.BIKF/"
    monkeypatch.setenv("FG_SCENERY", FG_SCENERY)
    monkeypatch.setattr("concat_ac3.FG_SCENERY", FG_SCENERY)

    concat_ac3.main(STGFile_path=stg_filepath)


def test_scale_factor():
    pass
