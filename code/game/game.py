import pygame

from code.program.states import FileStates


class Game:
    def __init__(self):
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

    def create_empty(self,
                     program,
                     ) -> None:
        self.set_file_name(
            program=program,
        )
        self.state = FileStates.EMPTY
    
    def set_file_name(self,
                      program,
                      new_file_name: str = None,
                      ) -> None:
        self.file_name = new_file_name
        program.set_caption(
            caption_1=self.file_name,
        )
        