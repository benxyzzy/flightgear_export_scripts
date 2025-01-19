#!/bin/sh

#Authors: J05HYYY

thepwd="$PWD"

FG_ROOT="${thepwd}/fgdata/fgdata/"

cd "${FG_ROOT}Scenery/SceneryPack.BIKF"

if [ -d "${FG_ROOT}Scenery/SceneryPack.BIKF/Master" ]; then
	rm -rf "${FG_ROOT}Scenery/SceneryPack.BIKF/Master"
fi

if [ -d "${FG_ROOT}Scenery/London/Master" ]; then
	rm -rf "${FG_ROOT}Scenery/London/Master"
fi

echo $PWD
find "${FG_ROOT}Scenery/London/Terrain" -maxdepth 2 -mindepth 2 -type d | while read tile; do
	mkdir -p "$(printf "Final/AC3D/%s\n" "$(printf "%s" $tile | rev | cut -d "/" -f 1-2 | rev)")"
	find "$tile" -type f | while read abtg; do


		mkdir -p "$(printf "%sScenery/SceneryPack.BIKF/Master/%s\n" "${FG_ROOT}" "$(printf "%s" $tile | rev | cut -d "/" -f 1-2 | rev)")"
		SCALE_FACTOR="1" FG_ROOT="${FG_ROOT}" FG_SCENERY="${FG_ROOT}Scenery/SceneryPack.BIKF/" python3 ${thepwd}/../btg_to_ac3d_2.py "${abtg}" "${FG_ROOT}Scenery/SceneryPack.BIKF/Master/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1)-objects.ac"

		masterstg="${FG_ROOT}Scenery/SceneryPack.BIKF/Master/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"

		printf "OBJECT_SHARED /Master/%s %s 0 0\n" "$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1)-objects.ac" "$(python3 ${thepwd}/../flightgear_tile.py $(printf "%s" "${abtg}" | rev | cut -d "/" -f 1 | rev | cut -d "." -f 1))" >> "$masterstg"

		astg="${FG_ROOT}Scenery/London/Objects/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"
		if [ -d "$(dirname "$astg")" ]; then
			if [ -f "$astg" ]; then
				cat "$astg" >> "$masterstg"
			fi
		fi

		astg="${FG_ROOT}Scenery/London/Pylons/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"
		if [ -d "$(dirname "$astg")" ]; then
			if [ -f "$astg" ]; then
				cat "$astg" >> "$masterstg"
			fi
		fi

		astg="${FG_ROOT}Scenery/London/Roads/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"
		if [ -d "$(dirname "$astg")" ]; then
			if [ -f "$astg" ]; then
				cat "$astg" >> "$masterstg"
			fi
		fi

		astg="${FG_ROOT}Scenery/London/Buildings/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"
		if [ -d "$(dirname "$astg")" ]; then

			if [ -f "$astg" ]; then
				cat "$astg" >> "$masterstg"
			fi
		fi

		astg="${FG_ROOT}Scenery/London/Details/$(printf "%s" "${abtg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).stg"
		if [ -d "$(dirname "$astg")" ]; then
			if [ -f "$astg" ]; then
				cat "$astg" >> "$masterstg"
			fi
		fi

		mkdir -p "$(printf "%s/Final/AC3D/%s\n" "${thepwd}" "$(printf "%s" $tile | rev | cut -d "/" -f 1-2 | rev)")"
		SCALE_FACTOR="0.001" FG_ROOT="${FG_ROOT}" FG_SCENERY="${FG_ROOT}Scenery/SceneryPack.BIKF/" python3 ${thepwd}/../concat_ac3.py "$masterstg" >> "${thepwd}/Final/AC3D/$(printf "%s" "${astg}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).ac"
	done
done

#find "${FG_ROOT}Scenery/SceneryPack.BIKF/Objects" -maxdepth 2 -mindepth 2 -type d | while read tile; do
#	mkdir -p "$(printf "Final/AC3D/%s\n" "$(printf "%s" $tile | rev | cut -d "/" -f 1-2 | rev)")"
#	find "$tile" -type f -name "*.stg" | while read astg; do
#		echo "OBJECT_SHARED $ac3d 0 0 0 0" >> "temp.stg"
#
#	done
#done

#find Terrain/AC3D/ -maxdepth 2 -mindepth 2 -type d | while read tile; do
#	mkdir -p "$(printf "Final/AC3D/%s\n" "$(printf "%s" $tile | rev | cut -d "/" -f 1-2 | rev)")"
#	find "$tile" -type f -name "*.ac" | while read ac3d; do
#		echo "OBJECT_SHARED $ac3d 0 0 0 0" >> "temp.stg"
#		find Objects -name "$(basename "$ac3d")" | while read objectFile; do
#		echo "OBJECT_SHARED $objectFile 0 0 0 0" >> "temp.stg"
#		dones
#		FG_ROOT="${thepwd}/" FG_SCENERY="${FG_ROOT}Scenery/SceneryPack.BIKF/Scenery" python3 ${thepwd}/../concat_ac3.py temp.stg > "Final/AC3D/$(printf "%s" "${ac3d}" | rev | cut -d "/" -f 1-3 | rev | cut -d "." -f 1).ac"
#		temp.stg
#	done
#done
