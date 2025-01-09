""" Calculate a FlightGear scenery tile index from a latitude and longitude

USAGE:

  $ python flightgear-tile.py LAT LON

Will print the index to standard output.

David Megginson, 2024-08-05 (Public Domain)


"""

from math import floor, trunc
import sys


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

def calculate_tile_index (lat, lon):
    """ Calculate the index for a lat/lon """
    
    tile_width = get_tile_width(lat)
    base_y = floor(lat)
    y = trunc((lat - base_y) * 8)
    base_x = floor(floor(lon / tile_width) * tile_width)
    x = floor((lon - base_x) / tile_width)
    index = ((base_x + 180) << 14) + ((base_y + 90) << 6) + (y << 3) + x

    return index

#
# Script entry point
#
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} LAT LON".format(sys.argv[0]), file=sys.stderr)
        exit(2)
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    if lat < -90 or lat > 90:
        print("Latitude {} out of range".format(lat))
        exit(1)
    if lon < -180 or lat > 180:
        print("Longitude {} out of range".format(lon))
        exit(1)
    print(calculate_tile_index(lat, lon))
    exit(0)