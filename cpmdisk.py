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

import struct
from collections import namedtuple

class CpmDisk:
    #block size
    #first data track
    #directory blocks
    #independent sides

    def __init__(self, block_size):
        super().__init__()
        self.block_size = block_size
        self.first_data_track = 0
        self.directory_blocks = 0
        self.sides = []
        self.sides.append(CpmDiskSide(0))
        self.sides.append(CpmDiskSide(1))
        self.independent_sides = False
        self.directory = CpmDirectory()

    def process_directory(self):
        directory_data=bytearray()
        directory_entries=[]
        skewed_sector = 0
        for i in range (self.directory_blocks):
            directory_data.extend(self.sides[0].tracks[self.first_data_track].sectors[skewed_sector].data)
            skewed_sector = skewed_sector + 5
            if skewed_sector > 8:
                skewed_sector = skewed_sector - 9
        
        for i in range (0,len(directory_data),32):
            directory_entry = namedtuple('directory_entry','user file type extent allocation')
            directory_entries.append(directory_entry._make(struct.unpack('<B8s3s4s16s',directory_data[i:i+32])))

        #All the text is in "directory Data"
        print(directory_data)



class CpmDiskSide:
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.tracks = []


class CpmTrack:
    #density
    #number of sectors
    #skew
    #sector size
    def __init__(self, density, number_of_sectors, skew, sector_size):
        super().__init__()
        self.density = density
        self.number_of_sectors = number_of_sectors
        self.skew = skew
        self.sector_size = sector_size
        self.sectors = []
        
        #sparse assignment of sectors...
        for x in range(0,self.number_of_sectors):
            self.sectors.append(None)


class CpmSector:
    #physical sector number
    #sector data
    def __init__(self, sector_number, data):
        super().__init__()
        self.sector_number = sector_number
        self.data = data

class CpmDirectory:
    pass

class CpmDirectoryEntry:
    pass