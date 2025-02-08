import pytest

from tile_calculator import calculate_tile_lon_lat, calculate_tile_index

def test_calculate_tile_lon_lat():
    """
    We test calculation of lon/lat from tile index
    by using calculate_tile_index()
    to get the correct index for known lon/lat.
    """
    completed_indices = []
    for expected_lat in range(-90, 90):
        for expected_lon in range(-180, 180):
            index = calculate_tile_index(expected_lat, expected_lon)
            if index in completed_indices:
                # Many lon/lat share the same index, so we only test each index once.
                # NOTE this means there are many lon/lat for which this test would fail,
                # because for a given index, we don't know exactly which lon/lat was
                # used to get it in the first place. Instead, calculate_tile_lon_lat()
                # can only return the lon/lat of the southwest corner of the specified
                # tile. The order that these for-loops iterate through their coords
                # is therefore important - by going in the positive direction we are
                # progressing north-easterly, hitting each tile's southwest corner first.
                continue

            actual_lat, actual_lon = calculate_tile_lon_lat(index)

            assert expected_lat == actual_lat
            assert expected_lon == actual_lon

            completed_indices.append(index)

def test_calculate_center_lon_lat():
    """Now calculate_tile_lon_lat() can return the coords of the center of the tile rather than southwest corner."""
    expected = (-156.3125, 20.8125)
    actual = calculate_tile_lon_lat(383925, return_center=True)
    assert expected == pytest.approx(actual)  # approx because of floating point imprecision
