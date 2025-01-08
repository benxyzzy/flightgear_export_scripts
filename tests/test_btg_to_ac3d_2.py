import os
from pathlib import Path

import pytest

from btg_to_ac3d_2 import main
from .utils import parse_verts_from_ac, reverse_scale_factor


def find_file(file_name, directory):
    for root, _, files in os.walk(directory):
        if file_name in files:
            return (Path(root) / file_name).resolve()
    return None


@pytest.fixture()
def btg_filepath():
    """
    This fixture looks for the stated BTG file anywhere within the project root or its subdirectories.
    You will need to copy the stated BTG file into the project somewhere, if it's not there already.
    If you don't have the stated BTG file, some other one (with verts) should work too - just change `btg_file`.
    Or if you don't want to copy it into the project, change `file_path` to the full path of the BTG file.
    """
    btg_file = "2582409.btg.gz"
    project_root = Path(__file__).resolve().parent.parent  # dir that contains tests/
    file_path = find_file(btg_file, project_root)
    if file_path:
        return file_path
    raise FileNotFoundError(f"The file '{btg_file}' was not found in the project root or its subdirectories.")
    

def test_scale_factor(btg_filepath, tmp_path, monkeypatch):
    """Run with different SCALE_FACTOR values and compare"""
    # FG_ROOT = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/"
    # monkeypatch.setenv("FG_ROOT", FG_ROOT)
    # monkeypatch.setattr("btg_to_ac3d_2.FG_ROOT", FG_ROOT)

    verts = {}
    for scale_factor in ("0.001", "0.05", "0.01", "0.1", "1", "2", "3"):
        monkeypatch.setenv("SCALE_FACTOR", scale_factor)

        outpath = tmp_path / f"test_scale_factor_{scale_factor}.ac"
        main(str(btg_filepath), str(outpath))

        with open(outpath, "r") as f:
            verts[scale_factor] = parse_verts_from_ac(f)

    # Test that SCALE_FACTOR has applied correctly by reversing it,
    # and checking that the (original) verts we get back are identical again
    orig_verts = reverse_scale_factor(verts)

    expected = next(iter(orig_verts.values()))  # just take one to compare against, we don't care which one
    for scale_factor, verts_list in orig_verts.items():
        for i in range(len(verts_list)):
            # approx due to float rounding error
            assert expected[i] == pytest.approx(verts_list[i]), \
                f"Expected verts to be identical for scale factor {scale_factor}"
