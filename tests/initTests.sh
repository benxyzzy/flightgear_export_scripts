#!/bin/sh
#Authors J05HYYY

thepwd="${PWD}"

mkdir Terrain
cd Terrain

#get BTG files

wget http://mirrors.ibiblio.org/flightgear/ftp/Scenery-v2.12/e000n50.tgz
tar -xf e000n50.tgz
mkdir -p BTG/e000n50/e000n51
cp -a Terrain/e000n50/e000n51/*.btg.gz BTG/e000n50/e000n51/
rm -rf Terrain Objects

wget http://mirrors.ibiblio.org/flightgear/ftp/Scenery-v2.12/w010n50.tgz
tar -xf w010n50.tgz
mkdir -p BTG/w010n50/w001n51
cp -a Terrain/w010n50/w001n51/*.btg.gz BTG/w010n50/w001n51/
rm -rf Terrain Objects

cd ..

#get Objects

mkdir Objects
cd Objects
git clone https://github.com/legoboyvdlp/London-OSM-fg-CustomScenery
mv London-OSM-fg-CustomScenery STG

cd ..

#get flightgear data

mkdir fgdata
cd fgdata
wget https://sourceforge.net/projects/flightgear/files/release-2020.3/FlightGear-2020.3.8-data.txz/download -O FlightGear-2020.3.8-data.txz
tar -xf FlightGear-2020.3.8-data.txz

cd ..

mkdir FG_ROOT
cd FG_ROOT
ln -s ../fgdata/fgdata/Models

#get conversion scripts #TODO:FIX BTG TO AC3D SCRIPT
#git clone https://github.com/publicsite/flightgear_export_scripts
#sed -i "s#FG_ROOT = \"/usr/share/games/flightgear/\"#FG_ROOT = \"${thepwd}/fgdata/fgdata/\"#g" flightgear_export_scripts/btg_to_ac3d_2.py
#sed -i "s#FG_ROOT = \"/usr/share/games/flightgear/\"#FG_ROOT = \"${thepwd}/fgdata/fgdata/\"#g" flightgear_export_scripts/concat_ac3.py
