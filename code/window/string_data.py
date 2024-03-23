from code.window.types import Types


class Strings:
    TITLE_TYPE = "resources/graphics/Roboto-Black.ttf"
    
    
class AskStrings:
    QUESTION_TYPE = Strings.TITLE_TYPE
    QUESTION_TEXTS = {
        Types.ASK_SAVE: "Would you like to save",
        Types.ASK_OVERWRITE: "Would you like to overwrite",
        Types.ASK_EXIT: "Would you like to exit",
    }
    BUTTON_TYPE = QUESTION_TYPE
    BUTTON_TEXTS = {
        Types.ASK_SAVE: ("Save", "No", "Cancel"),
        Types.ASK_OVERWRITE: ("Overwrite", "Save as", "Cancel"),
        Types.ASK_EXIT: ("Exit", "No", "Cancel"),
    }
    
    
class FileStrings:
    TITLE_TEXTS = {
        Types.SAVE: "Save",
        Types.SAVE_AS: "Save as",
        Types.LOAD: "Load",
    }
    BUTTON_TYPE = Strings.TITLE_TYPE
    BUTTON_TEXTS = {
        Types.SAVE: ("Save", "Cancel"),
        Types.SAVE_AS: ("Save", "Cancel"),
        Types.LOAD: ("Load", "Cancel"),
    }
    TEXTBOX_TYPE = BUTTON_TYPE
    
    
class ErrorUnopenedFileStrings:
    MESSAGE_TYPE = Strings.TITLE_TYPE
    MESSAGE_TEXT = "Please open a"
    BUTTON_TYPE = Strings.TITLE_TYPE
    BUTTON_TEXT = "OK"


class ErrorInvalidFileStrings:
    MESSAGE_TYPE = Strings.TITLE_TYPE
    MESSAGE_TEXT = "Invalid"
    BUTTON_TYPE = Strings.TITLE_TYPE
    BUTTON_TEXT = "OK"
