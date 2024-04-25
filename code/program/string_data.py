from code.program.types import FileTypes


class Strings:
    CAPTION = 'Rail Scheduler'
    FILE_TYPES = {
        FileTypes.NO: "",
        FileTypes.MAP: "map",
        FileTypes.SIM: "simulation",
        FileTypes.GAME: "game",
        FileTypes.SAVED_GAME: "saved game"
    }
    FILE_PASSWORDS = {
        FileTypes.MAP: bytes("This is a rail scheduler map   file", 'utf-8'),
        FileTypes.SIM: bytes("This is a rail scheduler sim   file", 'utf-8'),
        FileTypes.GAME: bytes("This is a rail scheduler game  file", 'utf-8'),
        FileTypes.SAVED_GAME: bytes("This is a rail scheduler sgame file", 'utf-8'),
    }
    