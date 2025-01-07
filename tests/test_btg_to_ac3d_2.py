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
    btg_file = "2582409.btg.gz"
    project_root = Path(__file__).resolve().parent.parent  # dir that contains tests/
    file_path = find_file(btg_file, project_root)
    if file_path:
        return file_path
    raise FileNotFoundError(f"The file '{btg_file}' was not found in the project root or its subdirectories.")
    

def test_scale_factor(btg_filepath, tmp_path, monkeypatch):
    """Run with different SCALE_FACTOR values and compare"""
    FG_ROOT = "/home/x/PycharmProjects/flightgear_export_scripts/fg_install/fgdata/fgdata/"
    monkeypatch.setenv("FG_ROOT", FG_ROOT)
    monkeypatch.setattr("btg_to_ac3d_2.FG_ROOT", FG_ROOT)

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

    from pprint import pprint
    pprint(verts)
