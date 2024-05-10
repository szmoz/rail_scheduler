import numpy as np

from code.program.states import FileStates
from code.program.string_data import Strings
from code.program.types import FileTypes


class Map:
    """
    Map object. Contains all map data and schedule data
    """
    def __init__(self):
        """
        Initialize an empty Map object
        """
        # Data
        self.data = {}
        self.data[4] = {}
        self.data[4][-120] = np.zeros(5, dtype=np.uint8)
        self.data[4][-120][0] = 0b00101011
        self.data[4][-120][1] = 38
        self.data[4][-120][2] = 23
        self.data[4][-120][3] = 67
        self.data[4][-120][4] = 9
        print(self.data)
        
        # File variables
        self.file_name = None
        self.file_state = FileStates.NO
        
    # Data management functions
    def load_data(self):
        """
        Load data from file
        """
        self.data.clear()
        with open("Files/Maps/" + self.file_name + ".rmap", "rb") as f:
            f.read(len(Strings.FILE_PASSWORDS[FileTypes.MAP]))
            while True:
                # Get coordinates
                coord_x = int.from_bytes(f.read(2), byteorder="big", signed=True)
                coord_y = int.from_bytes(f.read(2), byteorder="big", signed=True)
                # Check for end of file
                if 0 == coord_x == coord_y and coord_x in self.data.keys() and coord_y in self.data[0].keys():
                    break
                # Get selector and set length of tile data
                selector = int.from_bytes(f.read(1), byteorder="big", signed=False)
                count = 0
                for i in range(8):
                    if (selector >> i) & 1:
                        count += 1
                # Get tile data
                data_arr = np.zeros(count + 1, dtype=np.uint8)
                data_arr[0] = selector
                for i in range(1, count + 1, 1):
                    data_arr[i] = int.from_bytes(f.read(1), byteorder="big", signed=False)
                try:
                    self.data[coord_x][coord_y] = data_arr
                except KeyError:
                    self.data[coord_x] = {coord_y: data_arr}
        # Check for empty origo tile
        if 0 in self.data.keys() and 0 in self.data[0].keys() and len(self.data[0][0]) == 1:
            self.data[0].pop(0)
            if len(self.data[0]) == 0:
                self.data.pop(0)
            
    def save_data(self):
        """
        Save data to file
        """
        with open("Files/Maps/" + self.file_name + ".rmap", "wb") as f:
            password = Strings.FILE_PASSWORDS[FileTypes.MAP]
            f.write(password)
            for coord, tile_data in self.data.items():
                f.write(coord[0].to_bytes(2, byteorder="big", signed=True))
                f.write(coord[1].to_bytes(2, byteorder="big", signed=True))
                for data in tile_data:
                    f.write(int(data).to_bytes(1, byteorder="big", signed=False))
    
    # File handling functions
    def load(self,
             program,
             file_name: str,
             ) -> None:
        """
        Load map
        :param program: Program object
        :param file_name: name of map file to load
        """
        self.set_file_name(
            program=program,
            new_file_name=file_name,
        )
        self.load_data()
        self.file_state = FileStates.SAVED
    
    def save(self,
             program,
             file_name: str = None,
             ) -> None:
        """
        Save map
        :param program: Program object
        :param file_name: name of map file to save
        """
        if file_name is not None:
            self.set_file_name(
                program=program,
                new_file_name=file_name,
            )
        self.save_data()
        self.file_state = FileStates.SAVED
        
    def delete_progress(self) -> None:
        """
        Delete unsaved progress
        """
        self.file_state = FileStates.SAVED
        
    def create_empty(self, program) -> None:
        """
        Create empty map
        :param program: Program object
        """
        self.set_file_name(
            program=program,
        )
        self.file_state = FileStates.EMPTY
        
    def set_file_name(self,
                      program,
                      new_file_name: str = None,
                      ) -> None:
        """
        Set map file name and window caption
        :param program: Program object
        :param new_file_name: new map file name
        """
        self.file_name = new_file_name
        program.set_caption(
            caption_1=self.file_name,
        )
        