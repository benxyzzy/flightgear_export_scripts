import os
from pathlib import Path

import pytest

import concat_ac3
from .utils import parse_verts_from_ac, reverse_scale_factor

#Authors: benxyzzy


@pytest.fixture()
def stg_filepath():
    return (Path(__file__).parent / "958401-test.stg").resolve()


def test_concat_ac3(stg_filepath, monkeypatch):
    """High-level "smoke test" to check it runs without errors."""
    # FG_ROOT = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/"
    # monkeypatch.setenv("FG_ROOT", FG_ROOT)
    # monkeypatch.setattr("concat_ac3.FG_ROOT", FG_ROOT)
    #
    # FG_SCENERY = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/Scenery/SceneryPack.BIKF/"
    # monkeypatch.setenv("FG_SCENERY", FG_SCENERY)
    # monkeypatch.setattr("concat_ac3.FG_SCENERY", FG_SCENERY)

    concat_ac3.main(STGFile_path=stg_filepath)


def test_scale_factor(monkeypatch):
    """Run with different SCALE_FACTOR values and compare"""
    # FG_ROOT = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/"
    # monkeypatch.setenv("FG_ROOT", FG_ROOT)

    FG_ROOT = os.environ["FG_ROOT"]
    ACFilePath = str(Path(FG_ROOT) / 'Scenery/SceneryPack.BIKF/Models/Airport/thangar.ac')
    splitExtension = ['Models/Airport/thangar', 'ac']
    splitLine = ['OBJECT_SHARED', 'Models/Airport/thangar.ac', '-121.60000000', '37.0810000', '84.0', '204']

    verts = {}
    for scale_factor in ("0.001", "0.05", "0.01", "0.1", "1", "2", "3"):
        monkeypatch.setenv("SCALE_FACTOR", scale_factor)

        globalMaterials, mainBody, numberOfObjects = concat_ac3.processACFile(ACFilePath, splitExtension, splitLine)

        verts[scale_factor] = parse_verts_from_ac(mainBody)

    # Test that SCALE_FACTOR has applied correctly by reversing it,
    # and checking that the (original) verts we get back are identical again
    orig_verts = reverse_scale_factor(verts, divided=True)

    expected = next(iter(orig_verts.values()))  # just take one to compare against, we don't care which one
    for scale_factor, verts_list in orig_verts.items():
        for i in range(len(verts_list)):
            # approx due to float rounding error
            assert expected[i] == pytest.approx(verts_list[i]), \
                f"Expected verts to be identical for scale factor {scale_factor}"
