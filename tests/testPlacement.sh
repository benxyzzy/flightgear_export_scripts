#!/bin/sh

#Authors: J05HYYY

#sudo apt-get install blender flightgear openscenegraph

FG_ROOT=${FG_ROOT:-"/usr/share/games/flightgear/"}  # default if no env var
FG_ROOT="$(echo "$FG_ROOT" | sed 's~[^/]$~&/~')"  # add trailing slash if missing
export FG_ROOT

# can take input as arguments to the script (otherwise use original defaults)
stg=${1:-"${FG_ROOT}Scenery/Objects/w130n30/w122n37/958401.stg"}
btg_gz=${2:-"${FG_ROOT}Scenery/Terrain/w130n30/w122n37/958401.btg.gz"}

python3 ../concat_ac3.py "$stg" > objects1.ac
python3 ../btg_to_ac3d_2.py "$btg_gz" scenery1.ac
#osgconv objects1.ac out.obj

#visually check using flightgear that placement matches, or is similar enough...
#fgfs --fg-scenery=Scenery --enable-wireframe --lat=37.08390597 --lon=-121.60146087 --aircraft=ufo --console --log-level=info 2>&1 | tee fgfs.log
