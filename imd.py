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


class IMD:
    def __init__ (self, headertxt: str, comment: str):
        self.header = headertxt + comment + chr(0x1A)
        tracks=[]
        
    

class Track:
    def __init__(self, mode: int, cylinder: int, head: int, num_sectors: int, \
        sector_size: int, sector_map: int ):
        self.mode = mode
        self.cylinder = cylinder
        self.head = head
        self.num_sectors = num_sectors
        self.sector_size = sector_size
        self.sector_map = sector_map
        sectors = []


class Sector:
    def __init__(self, type_byte: int, data):
        pass