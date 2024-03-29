from code.program.types import FileTypes

from code.util.variable_data import CustomUserEvents as CustomETypes


FILE_DIR_PATHS = {
    FileTypes.MAP: "Files/Maps/",
    FileTypes.SIM: "Files/Simulations/",
    FileTypes.GAME: "Files/Games/",
    FileTypes.SAVED_GAME: "Files/Savefiles/"
}

FILE_EXTENSIONS = {
    FileTypes.MAP: ".rmap",
    FileTypes.SIM: ".rsim",
    FileTypes.GAME: ".rgame",
    FileTypes.SAVED_GAME: ".rgame",
}


class CustomEventTypes:
    WINDOW_BUTTON_CLICKED = CustomETypes.WINDOW_BUTTON_CLICKED


class FileWinFrameEdges:
    BUTTON_PRESSED = (3, 4)
    TEXTBOX = (-3, -4)
    LIST = TEXTBOX
    