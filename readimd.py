#   Copyright 2019 Daniel Jameson
#   This file is part of PythonCPM.
#
#   PythonCPM is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PythonCPM is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with PythonCPM.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import struct

sector_sizes = dict([ (0,128), (1,256), (2,512), (3,1024), (4,2048), \
    (5,4096), (6,8192) ])

def FileCheck(fn):
    try:
        open (fn,"r")
        return 1
    except IOError:
        print("\nNo such file.")
        return 0



parser=argparse.ArgumentParser(description="Load an IMD file")
parser.add_argument("filename", metavar="F", nargs=1, \
    help="File Name")
args=parser.parse_args()

# Check the file exists
file_name = args.filename[0]
result = FileCheck(file_name)
if result == 0 :
    exit()

# Open the file...
file=open(file_name, "rb")
header = bytearray()

while True:
    byte = file.read(1)
    if byte[0] == 0x1A:
        break
    else: 
        header.append(byte[0])

print(header)

# Track at a time...
while True:
    trackHeader = file.read(5)
    if not trackHeader:
        break
    
    trackMode = trackHeader[0]
    trackCylinder = trackHeader[1]
    trackHead = trackHeader[2]
    trackSectors = trackHeader[3]
    trackSectorSize = trackHeader[4]

    trackSectorMap = file.read(trackSectors)

    if trackHead & (1 << 7 ):
        trackCylMap = file.read(trackSectors)
    else:
        trackCylMap = None
    
    if trackHead & (1 << 6):
        trackHeadMap = file.read(trackSectors)
    else:
        trackHeadMap = None
    
    print("Track mode: ",trackMode)
    print("Cylinder: ",trackCylinder)
    print("Head: ",trackHead)
    print("Sectors: ",trackSectors)
    print("SectorSize: ",sector_sizes[trackSectorSize])
    print("SectorMap: ",trackSectorMap)
    if trackCylMap :
        print ("CylinderMap: ",trackCylMap)
    
    if trackHeadMap :
        print ("HeadMap: ",trackHeadMap)

    # for each sector
    for i in range(0,trackSectors):
        sectorStatus = file.read(1)[0]
        if (sectorStatus ==  1) or  (sectorStatus ==  3) or (sectorStatus ==  5) or \
            (sectorStatus ==  7):
            sectorData = file.read(sector_sizes[trackSectorSize])
        elif (sectorStatus ==  2) or  (sectorStatus ==  4) or (sectorStatus ==  6) or \
            (sectorStatus ==  8):
            sectorData = file.read(1)
        else:
            sectorData = None
        print("Sector ",i," Status: ",sectorStatus)
        print("Data:", sectorData)









