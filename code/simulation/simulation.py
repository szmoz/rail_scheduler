from code.program.states import FileStates


class Simulation:
    def __init__(self):
        self.file_name = ""
        self.state = FileStates.NO

    def load(self,
             file_name: str,
             ) -> None:
        self.file_name = file_name
        self.state = FileStates.SAVED

    def save(self,
             file_name: str = None,
             ) -> None:
        if file_name is not None:
            self.file_name = file_name
        self.state = FileStates.SAVED
        
    def delete_progress(self):
        self.state = FileStates.SAVED

    def create_empty(self):
        self.file_name = ""
        self.state = FileStates.EMPTY
    