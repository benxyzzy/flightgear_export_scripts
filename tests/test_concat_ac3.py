from pathlib import Path

import pytest

import concat_ac3

#Authors: benxyzzy


@pytest.fixture(params=[pytest.param(None, marks=pytest.mark.xfail(reason="This is not the correct test data"))])
def stg_filepath():
    # return Path("./958401.stg").resolve()
    return Path("./958401-test.stg").resolve()


def test_concat_ac3(stg_filepath):
    concat_ac3.main(STGFile_path=stg_filepath)
