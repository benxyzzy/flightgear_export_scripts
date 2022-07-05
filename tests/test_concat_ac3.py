import pytest

import concat_ac3

#Authors: benxyzzy


@pytest.fixture
def stg_filepath():
    return "./958401.stg"


def test_concat_ac3(stg_filepath):
    concat_ac3.main(STGFile_path=stg_filepath)
