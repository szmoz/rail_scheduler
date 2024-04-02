import pygame as pg

from code.program.states import FileStates


class Map:
    def __init__(self):
        # Data
        self.data = {}
        # File variables
        self.file_name = None
        self.state = FileStates.NO
    
    def load(self,
             program,
             file_name: str,
             ) -> None:
        self.set_file_name(
            program=program,
            new_file_name=file_name,
        )
        self.state = FileStates.SAVED
    
    def save(self,
             program,
             file_name: str = None,
             ) -> None:
        if file_name is not None:
            self.set_file_name(
                program=program,
                new_file_name=file_name,
            )
        self.state = FileStates.SAVED
        
    def delete_progress(self):
        self.state = FileStates.SAVED
        
    def create_empty(self, program):
        self.set_file_name(
            program=program,
        )
        self.state = FileStates.EMPTY
        
    def set_file_name(self,
                      program,
                      new_file_name: str = None,
                      ) -> None:
        self.file_name = new_file_name
        program.caption[1] = self.file_name
        program.caption[2] = None
        program.set_caption()
        