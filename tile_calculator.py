""" Calculate a FlightGear scenery tile index from a latitude and longitude

USAGE:

  $ python3 tile_calculator.py LON LAT

Will print the index to standard output.

OR

  $ python3 tile_calculator.py tile_index

Will print the LON LAT to standard output.

David Megginson, 2024-08-05 (Public Domain)
relicenced to GPLv2

"""

from math import floor, trunc
import sys

# Standard size of a bucket in degrees (1/8 of a degree)
SG_BUCKET_SPAN = 0.125
SG_HALF_BUCKET_SPAN = 0.5 * SG_BUCKET_SPAN


# Table of tile widths for various latitudes
TILE_WIDTHS = (
    (89, 90, 12,),
    (86, 89, 4,),
    (83, 86, 2,),
    (76, 83, 1,),
    (62, 76, 0.5,),
    (22, 62, 0.25,),
    (-22, 22, 0.125,),
    (-62, -22, 0.25,),
    (-76, -62, 0.5,),
    (-83, -76, 1,),
    (-86, -83, 2,),
    (-89, -86, 4,),
    (-90, -89, 12,),
)

def get_tile_width (lat):
    """ Calculate the tile width for a latitude """
    
    for entry in TILE_WIDTHS:
        if lat >= entry[0]:
            return entry[2]
    raise Exception("Latitude out of range")

def calculate_tile_index (lon, lat):
    """ Calculate the index for a lon/lat """
    
    tile_width = get_tile_width(lat)
    base_y = floor(lat)
    y = trunc((lat - base_y) * 8)
    base_x = floor(floor(lon / tile_width) * tile_width)
    x = floor((lon - base_x) / tile_width)
    index = ((base_x + 180) << 14) + ((base_y + 90) << 6) + (y << 3) + x

    return index

def calculate_tile_lon_lat(index: int, return_center: bool = False):
    """
    Calculate the lon/lat for a tile index (southwest corner OR center)

    Copied from SimGear SGBucket (newbucket.hxx; newbucket.cxx;
    1999 Curtis L. Olson - http://www.flightgear.org/~curt/ was the copyright holder)
    """

    # From SGBucket constructor
    lon = index >> 14
    index -= lon << 14
    lon -= 180

    lat = index >> 6
    index -= lat << 6
    lat -= 90

    y = index >> 3
    index -= y << 3

    x = index

    if return_center:
        # From get_center_lon()
        span = get_tile_width(lat)
        if span >= 1.0:
            lon = lon + span / 2.0
        else:
            lon = lon + x * span + span / 2.0

        # From get_center_lat()
        lat = lat + y / 8.0 + SG_HALF_BUCKET_SPAN

    return lon, lat

#
# Script entry point
#
if __name__ == '__main__':
    argv = sys.argv

    if argv[1] == "-c":  # we want the lon/lat of the center of the tile, not its southwest corner
        return_center = True
        argv = argv[1:]
    else:
        return_center = False

    if len(argv) == 2:
        index = int(argv[1])
        print(*calculate_tile_lon_lat(index, return_center))
    elif len(argv) == 3:
        if return_center:
            print("-c option not supported when asking for a tile index, ask for lon/lat instead")
            exit(1)

        lat = float(argv[1])
        lon = float(argv[2])
        if lat < -90 or lat > 90:
            print("Latitude {} out of range".format(lat))
            exit(1)
        if lon < -180 or lat > 180:
            print("Longitude {} out of range".format(lon))
            exit(1)

        print(calculate_tile_index(lat, lon))
    else:
        print(f"Usage:\n  python3 {argv[0]} <lat> <lon>\n  python3 {argv[0]} <index>", file=sys.stderr)
        exit(2)

    exit(0)
