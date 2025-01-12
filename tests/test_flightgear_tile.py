from flightgear_tile import calculate_tile_lat_lon, calculate_tile_index

def test_calculate_tile_lat_lon():
    """
    We test calculation of lat/lon from tile index
    by using calculate_tile_index()
    to get the correct index for known lat/lon.
    """
    completed_indices = []
    for expected_lat in range(-90, 90):
        for expected_lon in range(-180, 180):
            index = calculate_tile_index(expected_lat, expected_lon)
            if index in completed_indices:
                # Many lat/lon share the same index, so we only test each index once.
                # NOTE this means there are many lat/lon for which this test would fail,
                # because for a given index, we don't know exactly which lat/lon was
                # used to get it in the first place. Instead, calculate_tile_lat_lon()
                # can only return the lat/lon of the southwest corner of the specified
                # tile. The order that these for-loops iterate through their coords
                # is therefore important - by going in the positive direction we are
                # progressing north-easterly, hitting each tile's southwest corner first.
                continue

            actual_lat, actual_lon = calculate_tile_lat_lon(index)

            assert expected_lat == actual_lat
            assert expected_lon == actual_lon

            completed_indices.append(index)
