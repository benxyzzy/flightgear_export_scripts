from pathlib import Path

import pytest

import concat_ac3
from .utils import parse_verts_from_ac

#Authors: benxyzzy


@pytest.fixture()
def stg_filepath():
    return (Path(__file__).parent / "958401-test.stg").resolve()


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
    ACFilePath = '/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/Scenery/SceneryPack.BIKF/Models/Airport/thangar.ac'
    splitExtension = ['Models/Airport/thangar', 'ac']
    splitLine = ['OBJECT_SHARED', 'Models/Airport/thangar.ac', '-121.60000000', '37.0810000', '84.0', '204']

    globalMaterials, mainBody, numberOfObjects = concat_ac3.processACFile(ACFilePath, splitExtension, splitLine)

    verts = parse_verts_from_ac(mainBody)

    from pprint import pprint
    pprint(verts)
