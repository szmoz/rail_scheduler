class Sizes:
    TOPLINE_HEIGHT = 24
    TITLE = 16
    FRAME_THICKNESS = 5
    CORNER_BUTTON_GAP = 2
    CORNER_BUTTON_SIZE = TOPLINE_HEIGHT - (CORNER_BUTTON_GAP * 2)
    
    
class AskWinSizes:
    QUESTION = 20
    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 24
    BUTTON_FRAME_THICKNESS = 2
    BUTTON_TEXT = 16
    MIN_WIDTH = (Sizes.FRAME_THICKNESS * 2) + (BUTTON_WIDTH * 5)
    MAX_WIDTH = 800
    
    
class FileWinSizes:
    WIDTH = 500
    HEIGHT = 480
    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 24
    BUTTON_FRAME_THICKNESS = 2
    BUTTON_TEXT = 16
    TEXTBOX_HEIGHT = BUTTON_HEIGHT
    TEXTBOX_FRAME_THICKNESS = 2
    TEXTBOX_TEXT = BUTTON_TEXT
    