#!/usr/bin/python

import sys
import math

FG_ROOT = "/usr/share/games/flightgear/"

globalMaterials = []
mainBody = []
numberOfObjects = 0

def usage():
	print "Usage: python read_STG.py [file]"
	return

# Convert geoidic coordinates to cartesian
def geodToCart(lat, lon, alt):
	flattening = 298.257223563
	squash = (1 - 1/flattening)
	e2 = math.fabs(1-squash*squash)

	a = 6378137.0

	lambda1 = math.radians(lon)
	phi = math.radians(lat)
	h = alt

	sphi = math.sin(phi)

	n = a/math.sqrt(1-e2*sphi*sphi)
	cphi = math.cos(phi)
	slambda = math.sin(lambda1)
	clambda = math.cos(lambda1)
	x = (h+n)*cphi*clambda
	y = (h+n)*cphi*slambda
	z = (h+n-e2*n)*sphi
	return (x, y, z)

if len(sys.argv) <> 2:
	usage()
	sys.exit()

if FG_ROOT is not None:
	# Open a file
	STGFile = open(sys.argv[1], "r")
	#print "Reading: ", STGFile.name
	for line in STGFile: 
		splitLine = line.strip().split(" ");
		if len(splitLine) > 1:
			if splitLine[0] == "OBJECT_SHARED":
				splitExtension = splitLine[1].split(".")
				if splitExtension[len(splitExtension)-1] == "ac":
					materialsRelationship = []
					#print splitLine[1] #ac file name
					ACFile = open(FG_ROOT + splitLine[1], "r")
					for line2 in ACFile:
						if line2.strip() != "AC3Db":
							if line2.strip() == "OBJECT world":
								mainBody.append("OBJECT poly")
								mainBody.append("name \"_" + str(numberOfObjects) + "_" + splitExtension[0] +"\"")
								numberOfObjects = numberOfObjects + 1
								roll = 0
								heading = 0
								pitch = math.radians(90)
								if len(splitLine) < 7:
									heading = math.radians(float(splitLine[5]))
								elif len(splitLine) < 8:
									heading = math.radians(float(splitLine[5]))
									pitch = math.radians(float(splitLine[6])+90)
								elif len(splitLine) < 9:
									heading = math.radians(float(splitLine[5]))
									pitch = math.radians(float(splitLine[6])+90)
									roll = math.radians(float(splitLine[7]))

								ca = math.cos(roll)
								sa = math.sin(roll)
								cd = math.cos(heading)
								sd = math.sin(heading)
								cr = math.cos(pitch)
								sr = math.sin(pitch)

								rotationMatrix = ([[ca * cd, sa * cd, sd], [-ca * sd * sr - sa * cr,   -sa * sd * sr + ca * cr,   cd * sr], [-ca * sd * cr + sa * sr, -sa * sd * cr - ca * sr, cd * cr]])

								mainBody.append("rot " + str(rotationMatrix[0][0]) + " " + str(rotationMatrix[0][1]) + " " + str(rotationMatrix[0][2]) + " " + str(rotationMatrix[1][0]) + " " + str(rotationMatrix[1][1]) + " " + str(rotationMatrix[1][2]) + " " + str(rotationMatrix[2][0]) + " " + str(rotationMatrix[2][1]) + " " + str(rotationMatrix[2][2]))

								lat = float(splitLine[2])
								lon = float(splitLine[3])
								alt = float(splitLine[4])

								temp=geodToCart(37.5,-122.7,1000)

								convertedCoords = geodToCart(lat,lon,alt)

								mainBody.append("loc " + str(convertedCoords[1]) + " " + str(convertedCoords[2]) + " " + str(alt))
									#mainBody.append("loc " + str(lon) + " " + str(lat) + " " + str(rad))
							else:
								splitLine2 = line2.strip().split(" ");
								if len(splitLine2) > 0:
									if splitLine2[0] == "MATERIAL":
										found = -1
										for materialIndex in range(len(globalMaterials)):
											if globalMaterials[materialIndex] == line2.strip():
												found = 1;
												materialsRelationship.append(materialIndex)
												#print materialIndex
												break;
										if found == -1:
											materialsRelationship.append(len(globalMaterials))
											#print len(globalMaterials)
											globalMaterials.append(line2.strip())
									elif splitLine2[0] == "mat":
										if len(splitLine2) > 1:
											mainBody.append("mat " + str(materialsRelationship[int(splitLine2[1])]));
									else:
										mainBody.append(line2.strip())
					ACFile.close()

# Close opened file
STGFile.close()

print "AC3Db"
for materialIndex in range(len(globalMaterials)):
	print globalMaterials[materialIndex]
print "OBJECT world"
print "kids " + str(numberOfObjects)
for outputLine in mainBody:
	print outputLine