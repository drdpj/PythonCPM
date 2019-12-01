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

def file_check(fn):
    try:
        open (fn,"r")
        return 1
    except IOError:
        print("\nNo such file.\n")
        return 0



parser=argparse.ArgumentParser(description="Load an IMD file")
parser.add_argument("filename", metavar="F", nargs=1, \
    help="File Name")
args=parser.parse_args()

# Check the file exists
file_name = args.filename[0]
result = file_check(file_name)
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
# We assume that the file is the correct structure and we're
# parsing everything that could possibly be in there...

while True:
    track_header = file.read(5)
    if not track_header:
        break
    
    track_mode = track_header[0]
    track_cylinder = track_header[1]
    track_head = track_header[2]
    track_sectors = track_header[3]
    track_sector_size = track_header[4]

    track_sector_map = file.read(track_sectors)

    if track_head & (1 << 7 ):
        track_cyl_map = file.read(track_sectors)
    else:
        track_cyl_map = None
    
    if track_head & (1 << 6):
        track_head_map = file.read(track_sectors)
    else:
        track_head_map = None
    
    print("Track mode: ",track_mode)
    print("Cylinder: ",track_cylinder)
    print("Head: ",track_head)
    print("Sectors: ",track_sectors)
    print("SectorSize: ",sector_sizes[track_sector_size])
    print("SectorMap: ",track_sector_map)
    if track_cyl_map :
        print ("Cylinder Map: ",track_cyl_map)
    
    if track_head_map :
        print ("Head Map: ",track_head_map)

    # for each sector
    for i in range(0,track_sectors):
        sector_status_byte = file.read(1)[0]
        if (sector_status_byte ==  1) or  (sector_status_byte ==  3) or (sector_status_byte ==  5) or \
            (sector_status_byte ==  7):
            sector_data = file.read(sector_sizes[track_sector_size])
        elif (sector_status_byte ==  2) or  (sector_status_byte ==  4) or (sector_status_byte ==  6) or \
            (sector_status_byte ==  8):
            sector_data = file.read(1)
        else:
            sector_data = None
        print("Sector ",i," Status: ",sector_status_byte)
        print("Data:", sector_data)









