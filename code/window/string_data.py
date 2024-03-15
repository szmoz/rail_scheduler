class Strings:
    TITLE_TYPE = "resources/graphics/Roboto-Black.ttf"
    FILE_TYPES = {
        MenuProcessStates.Type.MAP: "map",
        MenuProcessStates.Type.SCH: "schedule",
        MenuProcessStates.Type.SIM: "simulation",
    }
    
    
class AskStrings:
    QUESTION_TYPE = Strings.TITLE_TYPE
    BUTTON_TYPE = QUESTION_TYPE
    BUTTON_TEXTS = {
        MenuProcessStates.Win.ASK_SAVE: ("Save", "No", "Cancel"),
        MenuProcessStates.Win.ASK_OW: ("Overwrite", "Save as", "Cancel"),
        MenuProcessStates.Win.ASK_EXIT: ("Exit", "No", "Cancel"),
    }
    
    
class FileStrings:
    BUTTON_TYPE = Strings.TITLE_TYPE
    BUTTON_TEXTS = {
        MenuProcessStates.Win.SAVE: ("Save", "Cancel"),
        MenuProcessStates.Win.SAVE_AS: ("Save", "Cancel"),
        MenuProcessStates.Win.LOAD: ("Load", "Cancel"),
    }
    