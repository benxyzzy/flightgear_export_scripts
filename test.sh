#!/bin/sh
#sudo apt-get install blender flightgear openscenegraph
./concat_ac3.py /usr/share/games/flightgear/Scenery/Objects/w130n30/w122n37/958401.stg > objects1.ac
python btg_to_ac3d_2.py /usr/share/games/flightgear/Scenery/Terrain/w130n30/w122n37/958401.btg.gz scenery1.ac
osgconv objects1.ac out.obj
fgfs --fg-scenery=Scenery --enable-wireframe --lat=37.08390597 --lon=-121.60146087 --aircraft=ufo --console --log-level=info 2>&1 | tee fgfs.log
