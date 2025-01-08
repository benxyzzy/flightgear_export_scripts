import os
from pathlib import Path

import pytest

from btg_to_ac3d_2 import main


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
        verts[scale_factor] = []
        monkeypatch.setenv("SCALE_FACTOR", scale_factor)

        outpath = tmp_path / f"test_scale_factor_{scale_factor}.ac"
        main(str(btg_filepath), str(outpath))

        # Parse out the verts for later comparison
        numvert = None
        verts_stored = None
        with open(outpath, "r") as f:
            for line in f:
                if numvert is not None:
                    # We're in a block of verts
                    verts[scale_factor].append([float(el) for el in line.split()])
                    verts_stored += 1
                    if verts_stored == numvert:
                        # end of block of verts
                        numvert = None
                        verts_stored = None
                else:
                    # We're not in a block of verts
                    if line.startswith("numvert"):
                        # block of verts found
                        numvert = int(line.split()[1])
                        verts_stored = 0

    # Test that SCALE_FACTOR has applied correctly by reversing it,
    # and checking that the (original) verts we get back are identical again
    orig_verts = {}
    for scale_factor, verts_list in verts.items():
        sf = float(scale_factor)
        orig_verts[scale_factor] = [
            [v/sf for v in verts]
            for verts in verts_list
        ]

    expected = next(iter(orig_verts.values()))  # just take one to compare against, we don't care which one
    for scale_factor, verts_list in orig_verts.items():
        for i in range(len(verts_list)):
            assert (
                expected[i] == pytest.approx(verts_list[i]),  # approx due to float rounding error
                f"Expected verts to be identical for scale factor {scale_factor}"
            )
