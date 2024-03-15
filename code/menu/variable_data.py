from code.program.states import FileStates
from code.program.types import FileTypes


class ButtonFrameEdgeLines:
    STANDARD = ([1, 2], [2], [2], [2], [2],)
    PRESSED = ([4], [4], [4], [4], [3, 4],)
    OVER = ([1, 2], [2], [2], [2], [2],)
    
    
inactive_menulist_elements = {
    FileTypes.NO * 10 + FileStates.EMPTY: {
        0: (1, 3, 4),
        1: (1, 3, 4, 5),
        2: (2, 3),
    },
    FileTypes.MAP * 10 + FileStates.EMPTY: {
        0: (0, 1, 4),
        1: (1, 3, 4, 5),
        2: (2, 3),
    },
    FileTypes.MAP * 10 + FileStates.NEW: {
        0: (1, 4),
        1: (1, 3, 4, 5),
        2: (2, 3),
    },
    FileTypes.MAP * 10 + FileStates.MOD: {
        0: (1, ),
        1: (1, 3, 4, 5),
        2: (2, 3),
    },
    FileTypes.MAP * 10 + FileStates.SAVED: {
        0: (1, 3),
        1: (1, 3, 4, 5),
        2: (2, 3),
    },
    FileTypes.SIM * 10 + FileStates.EMPTY: {
        0: (3, 4),
        1: (0, 1, 4, 5),
        2: (2, 3),
    },
    FileTypes.SIM * 10 + FileStates.NEW: {
        0: (3, 4),
        1: (1, 4),
        2: (2, 3),
    },
    FileTypes.SIM * 10 + FileStates.MOD: {
        0: (3, 4),
        1: (1, ),
        2: (2, 3),
    },
    FileTypes.SIM * 10 + FileStates.SAVED: {
        0: (3, 4),
        1: (1, 3),
        2: (2, 3),
    },
    FileTypes.GAME * 10 + FileStates.EMPTY: {
        0: (3, 4),
        1: (3, 4, 5),
        2: (3, ),
    },
    FileTypes.GAME * 10 + FileStates.NEW: {
        0: (3, 4),
        1: (3, 4),
        2: (3, ),
    },
    FileTypes.GAME * 10 + FileStates.MOD: {
        0: (3, 4),
        1: (3, 4),
        2: (),
    },
    FileTypes.GAME * 10 + FileStates.SAVED: {
        0: (3, 4),
        1: (3, 4),
        2: (2, ),
    },
}
