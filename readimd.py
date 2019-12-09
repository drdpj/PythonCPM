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
from cpmdisk import CpmDisk, CpmDiskSide, CpmTrack, CpmDirectory, CpmSector

sector_sizes = dict([ (0,128), (1,256), (2,512), (3,1024), (4,2048), \
    (5,4096), (6,8192) ])

def file_check(fn):
    try:
        open (fn,"r")
        return 1
    except IOError:
        print("\nNo such file.\n")
        return 0

def display_directory(d):
    disk = d
    disk.process_directory()

    for file_entry in disk.directory_entries:
        file_type = bytearray()
        rw = False
        sys = False
        for current_byte in file_entry.type:
            file_type.append(current_byte & 0b01111111)

        if (file_entry.type[0]>0x80):
            rw = True
        if (file_entry.type[1]>0x80):
            sys = True
        if (file_entry.file[0]<0x80):
            blocks = ""
            for x in file_entry.allocation:
                blocks = blocks + str(x) + " "
            print(file_entry.file.decode("ASCII")+"."+file_type.decode("ASCII"), end='')
            print(" "+str(rw)+" "+str(sys)+" "+str(file_entry.extent[0])+"-"+str(file_entry.extent[2])+" "+str(file_entry.extent[3])+" "+blocks)


parser=argparse.ArgumentParser(description="Load an IMD file")
parser.add_argument("filename", metavar="F", nargs=1, \
    help="File Name")
parser.add_argument("-d", action='store_true', help="display directory")
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

#block size for now... - RM480Z CP/M2.2
disk = CpmDisk(1024)
#directory size
disk.directory_blocks=4
#first data track
disk.first_data_track=3

while True:
    track_header = file.read(5)
    if not track_header:
        # File is finished...
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

    max_sector_value = max(track_sector_map)
    start_sector = max_sector_value - (track_sectors-1)
    current_track = CpmTrack(track_mode,track_sectors,0,sector_sizes[track_sector_size])
    current_side = disk.sides[(track_head & 1)]

    #fudge for RM images for the time being
    if track_cylinder == 0:
        current_track.skew=3
    else:
        current_track.skew=5

    
    if track_head_map :
        disk.independent_sides = True
        

    # for each sector
    for i in range(0,track_sectors):
        sector_status_byte = file.read(1)[0]
        sector_index_number = track_sector_map[i]-start_sector
        # Uncompressed sectors...
        if (sector_status_byte ==  1) or  (sector_status_byte ==  3) or (sector_status_byte ==  5) or \
            (sector_status_byte ==  7):
            sector_data = file.read(sector_sizes[track_sector_size])
            current_sector = CpmSector(track_sector_map[i], sector_data)
            current_track.sectors[sector_index_number] = current_sector
        # Compressed sectors...
        elif (sector_status_byte ==  2) or  (sector_status_byte ==  4) or (sector_status_byte ==  6) or \
            (sector_status_byte ==  8):
            sector_data = file.read(1)
            padded_data = bytearray()
            for x in range (0,sector_sizes[track_sector_size]):
                # fill up the sector with the given byte...
                padded_data.append(sector_data[0])
            current_sector = CpmSector(track_sector_map[i], padded_data)
            current_track.sectors[sector_index_number] = current_sector

        else:
            sector_data = None

    current_side.tracks.append(current_track)

print("Disk read into CpmDisk object.")
print("Tracks: ",len(disk.sides[0].tracks))

if args.d:
    display_directory(disk)






