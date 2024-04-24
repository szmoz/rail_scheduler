import pygame as pg

from code.program.states import FileStates


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
        
        # File variables
        self.file_name = None
        self.file_state = FileStates.NO
        
    # Data management functions
    
    
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
        program.caption[1] = self.file_name
        program.caption[2] = None
        program.set_caption()
        