import pygame as pg

from code.menu.types import MenuProcessTypes as ProcessTypes

from code.program.states import FileStates, ProgramSates
from code.program.string_data import Strings as ProgramStrings
from code.program.types import FileTypes

from code.util.states import TextBoxStates
from code.util.variable_data import CustomUserEvents

from code.window.ask_window import AskWindow
from code.window.error_window import ErrorWindow
from code.window.file_window import FileWindow
from code.window.string_data import AskStrings, ErrorUnopenedFileStrings, FileStrings
from code.window.types import Types as WinTypes


class MenuProcess:
    """
    Run menu processes
    """
    def __init__(self):
        """
        Initialize MenuProcess object
        """
        # 1. Current state
        # 2. button&element indexes
        # 3. steps
        # 4. button_idx
        self.processes = {
            FileTypes.NO * 10 + FileStates.EMPTY: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_empty}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_error_unopened_file_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1}},
                    1: {0: {'funct': self.load_file_create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_error_unopened_file_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1}},
                    1: {0: {'funct': self.load_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.load_file_create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
            },
            FileTypes.MAP * 10 + FileStates.EMPTY: {
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.create_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.create_new_save_as_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}},
                    2: {0: {'funct': self.save_file,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_error_unopened_file_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1}},
                    1: {0: {'funct': self.load_file_create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_error_unopened_file_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1}},
                    1: {0: {'funct': self.load_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.load_file_create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.MAP * 10 + FileStates.NEW: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 2}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP,
                                      'next_step': 2},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.create_new_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_error_unopened_file_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_error_unopened_file_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM,
                                      'next_step': 4},
                            'next_step': 5},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.load_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 5},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    3: {0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2}},
                    4: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 5},
                        1: {'funct': self.delete_last_window,
                            'param': {'next_step': 1}},
                        2: {'funct': self.delete_last_window,
                            'param': {'next_step': 1}},
                        3: {'funct': self.delete_last_window,
                            'param': {'next_step': 1}}},
                    5: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME,
                                      'next_step': 2},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME,
                                      'next_step': 2},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.MAP * 10 + FileStates.MOD: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.quick_save_file,
                        'param': {'close': True}}},
                FileTypes.MAP * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.delete_progress_create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.MAP * 10 + FileStates.SAVED: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_empty}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.SIM * 10 + FileStates.EMPTY: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.change_program_file_state_close_process,
                        'param': {'new_file_type': FileTypes.MAP,
                                  'new_file_state': FileStates.SAVED}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.MAP},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.change_program_file_state_close_process,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.create_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.create_new_save_as_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}},
                    2: {0: {'funct': self.save_file,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.SIM * 10 + FileStates.NEW: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.delete_progress_create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 2}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.delete_progress_change_program_file_state,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'next_step': 2,
                                      'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'next_step': 2,
                                      'file_type': FileTypes.MAP},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 2}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'next_step': 2,
                                      'file_type': FileTypes.SIM},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.create_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.CREATE_GAME: {
                    0: {'funct': self.create_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.save_file_create_new_save_window,
                            'param': {'next_step': 1,
                                      'file_type': FileTypes.GAME},
                            'next_step': 2},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}},
                    2: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'next_step': 3,
                                      'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME,
                                      'next_step': 2},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_name': "",
                                  'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 3},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME,
                                      'next_step': 2},
                            'next_step': 3},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 3},
                        1: {'funct': self.delete_last_window,
                            'next_step': 1},
                        2: {'funct': self.delete_last_window,
                            'next_step': 1},
                        3: {'funct': self.delete_last_window,
                            'next_step': 1}},
                    3: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.SIM * 10 + FileStates.MOD: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.delete_progress_change_program_file_state,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'next_step': 3,
                                      'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.quick_save_file,
                        'param': {'close': True}}},
                FileTypes.SIM * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.CREATE_GAME: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_save_window,
                            'param': {'next_step': 3,
                                      'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'next_step': 5,
                                      'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    5: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.delete_last_window,
                            'next_step': 4},
                        2: {'funct': self.delete_last_window,
                            'next_step': 4},
                        3: {'funct': self.delete_last_window,
                            'next_step': 4}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.SIM * 10 + FileStates.SAVED: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.change_program_file_state_close_process,
                            'param': {'new_file_type': FileTypes.MAP,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.SIM},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.SIM * 100 + ProcessTypes.CREATE_GAME: {
                    0: {'funct': self.create_new_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.save_file_change_program_file_state,
                            'param': {'next_step': 1,
                                      'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file_change_program_file_state,
                            'param': {'new_file_type': FileTypes.SIM,
                                      'new_file_state': FileStates.SAVED}},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}}},
            FileTypes.GAME * 10 + FileStates.MOD: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.load_from_game},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_load_from_game},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_load_from_game,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_load_from_game},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_empty},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_empty},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_empty,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_empty},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.SIM * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.load_from_game},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_load_from_game},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_load_from_game,
                            'param': {'next_step': 3}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_load_from_game},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_save_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_ask_overwrite_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 1},
                        1: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.quick_save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.create_new_save_window,
                            'param': {'file_type': FileTypes.GAME},
                            'next_step': 2},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    2: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME,
                                      'next_step': 3},
                            'next_step': 4},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    3: {0: {'funct': self.save_file_create_new_load_window,
                            'param': {'file_type': FileTypes.SAVED_GAME},
                            'next_step': 4},
                        1: {'funct': self.delete_last_window,
                            'next_step': 2},
                        2: {'funct': self.delete_last_window,
                            'next_step': 2},
                        3: {'funct': self.delete_last_window,
                            'next_step': 2}},
                    4: {0: {'funct': self.delete_progress_load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.SAVE: {
                    0: {'funct': self.quick_save_file,
                        'param': {'close': True}}},
                FileTypes.GAME * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}}},
            FileTypes.GAME * 10 + FileStates.SAVED: {
                FileTypes.MAP * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_from_game},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.MAP * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.MAP},
                            'next_step': 1},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_empty},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.EDIT: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_from_game},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}}},
                FileTypes.SIM * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_ask_exit_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.create_new_load_window,
                            'param': {'file_type': FileTypes.SIM},
                            'next_step': 1},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process},
                        3: {'funct': self.close_process}},
                    1: {0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.NEW: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.LOAD: {
                    0: {'funct': self.create_new_load_window,
                        'param': {'file_type': FileTypes.SAVED_GAME},
                        0: {'funct': self.load_file},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}}},
                FileTypes.GAME * 100 + ProcessTypes.SAVE_AS: {
                    0: {'funct': self.create_save_as_window,
                        'param': {'file_type': FileTypes.GAME},
                        0: {'funct': self.save_file,
                            'param': {'next_step': 1}},
                        1: {'funct': self.close_process},
                        2: {'funct': self.close_process}},
                    1: {0: {'funct': self.save_file},
                        1: {'funct': self.delete_last_window,
                            'next_step': 0},
                        2: {'funct': self.delete_last_window,
                            'next_step': 0},
                        3: {'funct': self.delete_last_window,
                            'next_step': 0}}}},
        }
        # Dynamic variables
        # Process
        self.process_file_type = FileTypes.NO
        self.process_type = ProcessTypes.NO
        self.process_code = -1
        self.init_file_code = -1
        self.step = 0
        # Window
        self.window = dict()
        self.current_win_idx = -1
    
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for menu process
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        # Window button clicked
        if event.type == CustomUserEvents.WINDOW_BUTTON_CLICKED:
            old_step = self.step
            params = {'program': program}
            try:
                for param_key, param in self.processes[self.init_file_code][self.process_code][self.step][event.button_idx]['param'].items():
                    params[param_key] = param
            except KeyError:
                pass
            self.processes[self.init_file_code][self.process_code][self.step][event.button_idx]['funct'](**params)
            try:
                if self.step == old_step:
                    self.step = self.processes[self.init_file_code][self.process_code][old_step][event.button_idx]['next_step']
                    print('change of step:', self.step)
            except KeyError:
                pass
            program.redraw = True
            program.break_event_loop = True
            return True
        # Window active
        if self.current_win_idx >= 0:
            return self.window[self.current_win_idx].event_manager(
                event=event,
                program=program
            )
        # Process function
        params = {'program': program}
        try:
            for param_key, param in self.processes[self.init_file_code][self.process_code][self.step]['param'].items():
                params[param_key] = param
        except KeyError:
            pass
        self.processes[self.init_file_code][self.process_code][self.step]['funct'](**params)
        program.redraw = True
        program.break_event_loop = True
        return True
        
    # Main process functions
    def start_new_process(self,
                          menubar_button_idx: int,
                          list_element_idx: int,
                          program,
                          ) -> None:
        """
        Start new menu process
        :param menubar_button_idx: pressed menubar button index
        :param list_element_idx: clicked menulist element index
        :param program: Program object
        """
        print('start_new_process', self.step, program.file_type, program.file_state, menubar_button_idx, list_element_idx)
        self.process_file_type = menubar_button_idx + 1
        self.process_type = list_element_idx
        if self.process_file_type == FileTypes.GAME and self.process_type > ProcessTypes.NEW:
            self.process_type += 1
        self.set_process_code()
        self.init_file_code = program.get_file_code()
        program.state = ProgramSates.WINDOW
        self.event_manager(
            event=pg.event.Event(CustomUserEvents.START_MENU_PROCESS),
            program=program
        )
        print('start_new_process end:', self.step, program.file_type, program.file_state)
        
    def close_process(self,
                      program,
                      ) -> None:
        """
        Close actual menu process
        :param program: Program object
        """
        print('close_process', self.step, program.file_type, program.file_state)
        self.process_file_type = FileTypes.NO
        self.process_type = ProcessTypes.NO
        self.step = 0
        self.delete_all_windows(program)
        program.state = program.isopened
        print('close_process end:', self.step, program.file_type, program.file_state)
        
    def change_program_file_state_close_process(self,
                                                program,
                                                new_file_type: int = None,
                                                new_file_state: int = None,
                                                ) -> None:
        """
        Change program state and close process
        :param program: Program object
        :param new_file_type: new file type
        :param new_file_state: new file state
        """
        print('change_program_file_state_close_process', self.step, program.file_type, program.file_state, new_file_type, new_file_state)
        self.change_program_file_state(
            program=program,
            new_file_type=new_file_type,
            new_file_state=new_file_state
        )
        self.close_process(program)
        print('change_program_file_state_close_process end:', self.step, program.file_type, program.file_state)
        
    def set_process_code(self) -> None:
        """
        Set process code: process file type * 100 + process type
        """
        self.process_code = self.process_file_type * 100 + self.process_type
        
    # Window functions
    def create_new_load_window(self,
                               program,
                               file_type: int,
                               ) -> None:
        """
        Delete all windows and Create load file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_new_load_window', self.step, program.file_type, program.file_state, file_type)
        self.delete_all_windows(program)
        self.create_load_window(
            program=program,
            file_type=file_type)
        print('create_new_load_window end:', self.step, program.file_type, program.file_state)
        
    def load_file_create_new_load_window(self,
                                         program,
                                         file_type: int,
                                         ) -> None:
        """
        Load file and create new load window
        :param program: Program object
        :param file_type: file type code
        """
        print('load_file_create_new_load_window', self.step, program.file_type, program.file_state, file_type)
        if not self.load_file(program, close=False):
            print('load_file_create_new_load_window end:', self.step, program.file_type, program.file_state)
            return
        self.create_new_load_window(program, file_type)
        print('load_file_create_new_load_window end:', self.step, program.file_type, program.file_state)
        
    def save_file_create_new_load_window(self,
                                         program,
                                         file_type: int,
                                         next_step: int = None,
                                         ) -> None:
        """
        Save file and create new load window
        :param program: Program object
        :param file_type: file type code
        :param next_step: next step, when overwrite needed
        """
        print('save_file_create_new_load_window', self.step, program.file_type, program.file_state, file_type, next_step)
        if not self.save_file(
                program=program,
                next_step=next_step,
                close=False):
            print('save_file_create_new_load_window end:', self.step, program.file_type, program.file_state)
            return
        self.create_new_load_window(program, file_type)
        print('save_file_create_new_load_window end:', self.step, program.file_type, program.file_state)
        
    def quick_save_file_create_new_load_window(self,
                                               program,
                                               file_type: int,
                                               ) -> None:
        """
        Quick save file and create new load window
        :param program: Program object
        :param file_type: file type code for load window
        """
        print('quick_save_file_create_new_load_window', self.step, program.file_type, program.file_state, file_type)
        self.quick_save_file(program)
        self.create_new_load_window(program, file_type)
        print('quick_save_file_create_new_load_window end:', self.step, program.file_type, program.file_state)
        
    def create_load_window(self,
                           program,
                           file_type: int,
                           ) -> None:
        """
        Create load file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_load_window', self.step, program.file_type, program.file_state, file_type)
        self.current_win_idx += 1
        self.window[self.current_win_idx] = FileWindow(
            win_type=WinTypes.LOAD,
            file_type=file_type,
            screen_center=program.screen.get_rect().center,
            title=f'{FileStrings.TITLE_TEXTS[WinTypes.LOAD]} '
                  f'{ProgramStrings.FILE_TYPES[file_type]}',
            start_text="",
        )
        self.window[self.current_win_idx].textbox.state = TextBoxStates.CURSOR
        self.window[self.current_win_idx].textbox.activate_cursor(
            program=program,
            new_cursor_pos=0,
        )
        print('create_load_window end:', self.step, program.file_type, program.file_state)
        
    def create_new_save_window(self,
                               program,
                               file_type: int,
                               ) -> None:
        """
        Delete all windows and Create save file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_new_save_window', self.step, program.file_type, program.file_state, file_type)
        self.delete_all_windows(program)
        self.create_save_window(
            program=program,
            file_type=file_type)
        print('create_new_save_window end:', self.step, program.file_type, program.file_state)
        
    def create_save_window(self,
                           program,
                           file_type: int,
                           ) -> None:
        """
        Create save file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_save_window', self.step, program.file_type, program.file_state, file_type)
        self.current_win_idx += 1
        self.window[self.current_win_idx] = FileWindow(
            win_type=WinTypes.SAVE,
            file_type=file_type,
            screen_center=program.screen.get_rect().center,
            title=f'{FileStrings.TITLE_TEXTS[WinTypes.SAVE]} '
                  f'{ProgramStrings.FILE_TYPES[file_type]}',
            start_text="",
        )
        self.window[self.current_win_idx].textbox.state = TextBoxStates.CURSOR
        self.window[self.current_win_idx].textbox.activate_cursor(
            program=program,
            new_cursor_pos=0,
        )
        print('create_save_window end:', self.step, program.file_type, program.file_state)
        
    def save_file_create_new_save_window(self,
                                         program,
                                         file_type: int,
                                         next_step: int = None,
                                         ) -> None:
        """
        Save file and create new save window
        :param program: Program object
        :param next_step: next step if need to overwrite; if None: no file name precheck
        :param file_type: file type code for new save window
        """
        print('save_file_create_new_save_window', self.step, program.file_type, program.file_state, file_type, next_step)
        if not self.save_file(
                program=program,
                next_step=next_step,
                close=False):
            print('save_file_create_new_save_window end:', self.step, program.file_type)
            return
        self.create_new_save_window(
            program=program,
            file_type=file_type,
        )
        print('save_file_create_new_save_window end:', self.step, program.file_type)
        
    def quick_save_file_create_new_save_window(self,
                                               program,
                                               file_type: int,
                                               ) -> None:
        """
        Quick save file and create new save window
        :param program: Program object
        :param file_type: file type code for new save window
        """
        print('quick_save_file_create_new_save_window', self.step, program.file_type, program.file_state, file_type)
        self.quick_save_file(program=program, close=False)
        self.create_new_save_window(
            program=program,
            file_type=file_type,
        )
        print('quick_save_file_create_new_save_window end:', self.step, program.file_type)

    def create_new_save_as_window(self,
                                  program,
                                  file_type: int,
                                  ) -> None:
        """
        Delete all windows and Create save as file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_new_save_as_window', self.step, program.file_type, program.file_state, file_type)
        self.delete_all_windows(program)
        self.create_save_as_window(
            program=program,
            file_type=file_type)
        print('create_new_save_as_window end:', self.step, program.file_type, program.file_state)

    def create_save_as_window(self,
                              program,
                              file_type: int,
                              ) -> None:
        """
        Create save as file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_save_as_window', self.step, program.file_type, program.file_state, file_type)
        self.current_win_idx += 1
        self.window[self.current_win_idx] = FileWindow(
            win_type=WinTypes.SAVE_AS,
            file_type=file_type,
            screen_center=program.screen.get_rect().center,
            title=f'{FileStrings.TITLE_TEXTS[WinTypes.SAVE_AS]} '
                  f'{ProgramStrings.FILE_TYPES[file_type]}',
            start_text="",
        )
        start_text = program.files[program.file_type].file_name
        if start_text is None:
            start_text = ""
        self.window[self.current_win_idx].textbox.change_text_highlight_all(
            new_text=start_text,
            program=program,
        )
        self.window[self.current_win_idx].list.update_list(
            surf=program.screen,
            new_clicked_idx=self.window[self.current_win_idx].list.find_name(
                name=start_text,
            ),
        )
        print('create_save_as_window end:', self.step, program.file_type, program.file_state)
    
    def create_ask_save_window(self,
                               program,
                               file_type: int,
                               file_name: str = None,
                               ) -> None:
        """
        Create ask save window
        :param program: Program object
        :param file_name: file name
        :param file_type: file type code
        """
        print('create_ask_save_window', self.step, program.file_type, program.file_state, file_type, file_name)
        if file_name is None:
            file_name = program.files[file_type].file_name
            if file_name is None:
                file_name = "the"
        elif file_name == "":
            file_name = "the"
        self.current_win_idx += 1
        self.window[self.current_win_idx] = AskWindow(
            win_type=WinTypes.ASK_SAVE,
            screen_center=program.screen.get_rect().center,
            question=f'{AskStrings.QUESTION_TEXTS[WinTypes.ASK_SAVE]} '
                     f'{file_name} {ProgramStrings.FILE_TYPES[file_type]}?'
        )
        print('create_ask_save_window end:', self.step, program.file_type, program.file_state)
        
    def create_ask_overwrite_window(self,
                                    program,
                                    file_type: int,
                                    file_name: str = None,
                                    ) -> None:
        """
        Create ask overwrite window
        :param program: Program object
        :param file_name: file name
        :param file_type: file type code
        """
        print('create_ask_overwrite_window', self.step, program.file_type, program.file_state, file_type, file_name)
        if file_name is None:
            file_name = program.files[file_type].file_name
        self.current_win_idx += 1
        self.window[self.current_win_idx] = AskWindow(
            win_type=WinTypes.ASK_OVERWRITE,
            screen_center=program.screen.get_rect().center,
            question=f'{AskStrings.QUESTION_TEXTS[WinTypes.ASK_OVERWRITE]} '
                     f'{file_name} {ProgramStrings.FILE_TYPES[file_type]}?'
        )
        print('create_ask_overwrite_window end:', self.step, program.file_type, program.file_state)

    def create_new_ask_overwrite_window(self,
                                        program,
                                        file_type: int,
                                        file_name: str = None,
                                        ) -> None:
        """
        Create new ask overwrite window
        :param program: Program object
        :param file_name: file name
        :param file_type: file type code
        """
        print('create_new_ask_overwrite_window', self.step, program.file_type, program.file_state, file_type, file_name)
        self.delete_all_windows()
        self.create_ask_overwrite_window(
            program=program,
            file_type=file_type,
            file_name=file_name
        )
        print('create_new_ask_overwrite_window end:', self.step, program.file_type, program.file_state)

    def create_ask_exit_window(self,
                               program,
                               file_type: int,
                               file_name: str = None,
                               ) -> None:
        """
        Create ask exit window
        :param program: Program object
        :param file_name: file name
        :param file_type: file type code
        """
        print('create_ask_exit_window', self.step, program.file_type, program.file_state, file_type, file_name)
        if file_name is None:
            file_name = program.files[file_type].file_name
            if file_name is None:
                file_name = "the"
        self.current_win_idx += 1
        self.window[self.current_win_idx] = AskWindow(
            win_type=WinTypes.ASK_EXIT,
            screen_center=program.screen.get_rect().center,
            question=f'{AskStrings.QUESTION_TEXTS[WinTypes.ASK_EXIT]} '
                     f'{file_name} {ProgramStrings.FILE_TYPES[file_type]}?'
        )
        print('create_ask_exit_window end:', self.step, program.file_type, program.file_state)

    def create_new_ask_exit_window(self,
                                   program,
                                   file_type: int,
                                   file_name: str = None,
                                   ) -> None:
        """
        Create new ask exit window
        :param program: Program object
        :param file_type: file type code
        :param file_name: file name
        """
        print('create_new_ask_exit_window', self.step, program.file_type, program.file_state, file_type, file_name)
        self.delete_all_windows()
        self.create_ask_exit_window(
            program=program,
            file_type=file_type,
            file_name=file_name,
        )
        print('create_new_ask_exit_window end:', self.step, program.file_type, program.file_state)
    
    def create_error_unopened_file_window(self,
                                          program,
                                          file_type: int,
                                          ) -> None:
        """
        Create error unopened file window
        :param program: Program object
        :param file_type: file type code
        """
        print('create_error_unopened_file_window', self.step, program.file_type, program.file_state, file_type)
        self.current_win_idx += 1
        self.window[self.current_win_idx] = ErrorWindow(
            win_type=WinTypes.ERROR_UNOPENED_FILE,
            error_message=f'{ErrorUnopenedFileStrings.MESSAGE_TEXT} '
                          f'{ProgramStrings.FILE_TYPES[file_type]}!',
            screen_center=program.screen.get_rect().center,
        )
        print('create_error_unopened_file_window end:', self.step, program.file_type, program.file_state)

    def delete_last_window(self,
                           next_step: int = None,
                           *args, **kwargs) -> None:
        """
        Delete last window
        """
        print('delete_last_window', self.step, next_step)
        self.window.pop(self.current_win_idx)
        self.current_win_idx -= 1
        if next_step is not None:
            self.step = next_step
        print('delete_last_window end:', self.step)

    def delete_all_windows(self,
                           *args, **kwargs) -> None:
        """
        Delete all windows
        """
        print('delete_all_windows', self.step)
        self.window.clear()
        self.current_win_idx = -1
        print('delete_all_windows end:', self.step)
        
    # During process functions
    def change_program_file_state(self,
                                  program,
                                  new_file_type: int = None,
                                  new_file_state: int = None,
                                  ) -> None:
        """
        Change program state
        :param program: Program object
        :param new_file_type: new file type
        :param new_file_state: new file state
        """
        print('change_program_file_state', self.step, program.file_type, program.file_state, new_file_type, new_file_state)
        if new_file_type is not None and program.file_type != new_file_type:
            program.file_type = new_file_type
            program.files[program.file_type].set_file_name(
                program=program,
                new_file_name=program.files[program.file_type].file_name,
            )
            program.camera.view.change_file_type(new_file_type=new_file_type)
        if new_file_state is not None:
            program.file_state = new_file_state
        program.isopened = ProgramSates.OPENED_BASIC
        program.menu.set_inactive_list_elements(program)
        print('change_program_file_state end:', self.step, program.file_type, program.file_state)

    def delete_progress(self,
                        program,
                        file_type: int = None) -> None:
        """
        Delete progress on actual file
        :param program: Program object
        :param file_type: file type that needs delete in progress. If None: actual file
        """
        print('delete_progress', self.step, program.file_type, program.file_state, file_type)
        if file_type is None:
            file_type = program.file_type
        program.files[file_type].delete_progress()
        print('delete_progress end:', self.step, program.file_type, program.file_state)
    
    # Process End functions
    def delete_progress_change_program_file_state(self,
                                                  program,
                                                  act_file_type: int = None,
                                                  new_file_type: int = None,
                                                  new_file_state: int = None,
                                                  ) -> None:
        """
        Delete progress and change program state
        :param program: Program object
        :param act_file_type: file type that needs delete in progress. If None: actual file
        :param new_file_type: new file type
        :param new_file_state: new file state
        """
        print('delete_progress_change_program_file_state', self.step, program.file_type, program.file_state, act_file_type, new_file_type, new_file_state)
        self.delete_progress(
            program=program,
            file_type=act_file_type
        )
        self.change_program_file_state(
            program=program,
            new_file_type=new_file_type,
            new_file_state=new_file_state
        )
        self.close_process(program)
        print('delete_progress_change_program_file_state end:', self.step, program.file_type, program.file_state)
        
    def create_empty(self,
                     program,
                     ) -> None:
        """
        Create empty file
        :param program: Program object
        """
        print('create_empty', self.step, program.file_type, program.file_state)
        program.files[self.process_file_type].create_empty(program=program)
        self.change_program_file_state(
            program=program,
            new_file_type=self.process_file_type,
            new_file_state=FileStates.EMPTY
        )
        self.close_process(program)
        print('create_empty end:', self.step, program.file_type, program.file_state)

    def delete_progress_create_empty(self,
                                     program,
                                     ) -> None:
        """
        Delete progress in actual file and create empty file
        :param program: Program object
        """
        print('delete_progress_create_empty', self.step, program.file_type, program.file_state)
        self.delete_progress(program)
        self.create_empty(program)
        print('delete_progress_create_empty end:', self.step, program.file_type, program.file_state)

    def load_file(self,
                  program,
                  close: bool = True,
                  ) -> bool:
        """
        Load file if given file name is existing
        :param program: Program object
        :param close: True: close process; False: do not close process
        :return True: file name existing; False: file name not existing
        """
        print('load_file', self.step, program.file_type, program.file_state, close)
        if not self.window[self.current_win_idx].is_file_name_exist():
            print('load_file end:', self.step, program.file_type, program.file_state)
            return False
        file_idx = self.window[self.current_win_idx].file_type
        if file_idx > FileTypes.GAME:
            file_idx = FileTypes.GAME
        program.files[file_idx].load(
            program=program,
            file_name=self.window[self.current_win_idx].textbox.text.text,
        )
        self.change_program_file_state(
            program=program,
            new_file_type=file_idx,
            new_file_state=FileStates.SAVED,
        )
        if close:
            self.close_process(program)
        print('load_file end:', self.step, program.file_type, program.file_state)
        return True
        
    def load_file_create_empty(self,
                               program,
                               ) -> None:
        """
        Load file if given file name is existing and create new empty file (different type than loaded file)
        :param program: Program object
        """
        print('load_file_create_empty', self.step, program.file_type, program.file_state)
        if not self.load_file(program, close=False):
            print('load_file_create_empty end:', self.step, program.file_type, program.file_state)
            return
        self.create_empty(program)
        print('load_file_create_empty end:', self.step, program.file_type, program.file_state)

    def delete_progress_load_file(self,
                                  program,
                                  ) -> None:
        """
        Delete progress in actual file and load file
        :param program: Program object
        """
        print('delete_progress_load_file', self.step, program.file_type, program.file_state)
        old_file_type = program.file_type
        if not self.load_file(program):
            print('delete_progress_load_file end:', self.step, program.file_type, program.file_state)
            return
        self.delete_progress(program, file_type=old_file_type)
        print('delete_progress_load_file end:', self.step, program.file_type, program.file_state)
        
    def load_from_game(self,
                       program,
                       ) -> None:
        """
        Load file from saved game
        :param program: Program object
        """
        print('load_from_game', self.step, program.file_type, program.file_state)
        self.change_program_file_state_close_process(
            program=program,
            new_file_type=self.process_file_type,
            new_file_state=FileStates.NEW,
        )
        print('load_from_game end:', self.step, program.file_type, program.file_state)

    def save_file(self,
                  program,
                  next_step: int = None,
                  close: bool = True,
                  ) -> bool:
        """
        Check if given file name exists, if yes: create ask overwrite window. if not: save file
        :param program: Program object
        :param next_step: next step if need to overwrite; if None: no file name precheck
        :param close: True: close process; False: do not close process
        :return True: file name not existing; False: file name existing, overwrite ask window needed
        """
        print('save_file', self.step, program.file_type, program.file_state, next_step, close)
        if next_step is not None and self.window[self.current_win_idx].is_file_name_exist():
            self.step = next_step
            self.create_ask_overwrite_window(
                program=program,
                file_name=self.window[self.current_win_idx].textbox.text.text,
                file_type=self.window[self.current_win_idx].file_type,
            )
            print('save_file end:', self.step, program.file_type, program.file_state)
            return False
        win_idx = self.current_win_idx
        if len(self.window) > 1:
            win_idx -= 1
        file_idx = self.window[win_idx].file_type
        if file_idx > FileTypes.GAME:
            file_idx = FileTypes.GAME
        if self.current_win_idx > 0:
            file_name = self.window[0].textbox.text.text
        else:
            file_name = self.window[self.current_win_idx].textbox.text.text
        program.files[file_idx].save(
            program=program,
            file_name=file_name
        )
        self.change_program_file_state(
            program=program,
            new_file_type=file_idx,
            new_file_state=FileStates.SAVED
        )
        if close:
            self.close_process(program)
        print('save_file end:', self.step, program.file_type, program.file_state)
        return True
    
    def save_file_create_empty(self,
                               program,
                               next_step: int = None,
                               ) -> None:
        """
        Check if given file name exists, if yes: create ask overwrite window. if not: save file and create empty
        :param program: Program object
        :param next_step: next step if need to overwrite; if None: no file name precheck
        """
        print('save_file_create_empty', self.step, program.file_type, program.file_state, next_step)
        if not self.save_file(program=program, next_step=next_step, close=False):
            print('save_file_create_empty end:', self.step, program.file_type, program.file_state)
            return
        self.create_empty(program)
        print('save_file_create_empty end:', self.step, program.file_type, program.file_state)
        
    def save_file_change_program_file_state(self,
                                            program,
                                            next_step: int = None,
                                            new_file_type: int = None,
                                            new_file_state: int = None,
                                            ) -> None:
        """
        Save file and change program state
        :param program: Program object
        :param next_step: next step if need to overwrite; if None: no file name precheck
        :param new_file_type: new file type
        :param new_file_state: new file state
        """
        print('save_file_change_program_file_state', self.step, program.file_type, program.file_state, next_step, new_file_type, new_file_state)
        if not self.save_file(program=program, next_step=next_step, close=False):
            print('save_file_change_program_file_state end:', self.step, program.file_type, program.file_state)
            return
        self.change_program_file_state(
            program=program,
            new_file_type=new_file_type,
            new_file_state=new_file_state,
        )
        self.close_process(program=program)
        print('save_file_change_program_file_state end:', self.step, program.file_type, program.file_state)
        
    def save_file_load_from_game(self,
                                 program,
                                 next_step: int = None,
                                 ) -> None:
        """
        Check if given file name exists, if yes: create ask overwrite window. if not: save file and load file from game
        :param program: Program object
        :param next_step: next step if need to overwrite; if None: no file name precheck
        """
        print('save_file_load_from_game', self.step, program.file_type, program.file_state, next_step)
        if not self.save_file(program=program, next_step=next_step, close=False):
            print('save_file_load_from_game end:', self.step, program.file_type, program.file_state)
            return
        self.load_from_game(program)
        print('save_file_load_from_game end:', self.step, program.file_type, program.file_state)

    def quick_save_file(self,
                        program,
                        close: bool = False,
                        ) -> None:
        """
        Quick save opened, actual file
        :param program: Program object
        :param close: True: close process
        """
        print('quick_save_file', self.step, program.file_type, program.file_state, close)
        program.files[program.file_type].save(program=program)
        self.change_program_file_state(
            program=program,
            new_file_state=FileStates.SAVED,
        )
        if close:
            self.close_process(program)
        print('quick_save_file end:', self.step, program.file_type, program.file_state)
        
    def quick_save_file_create_empty(self,
                                     program,
                                     ) -> None:
        """
        Quick save opened, actual file and create empty file
        :param program: Program object
        """
        print('quick_save_file_create_empty', self.step, program.file_type, program.file_state)
        self.quick_save_file(program)
        self.create_empty(program)
        print('quick_save_file_create_empty end:', self.step, program.file_type, program.file_state)

    def quick_save_file_change_program_file_state(self,
                                                  program,
                                                  new_file_type: int = None,
                                                  new_file_state: int = None,
                                                  ) -> None:
        """
        Quick save file and change program state
        :param program: Program object
        :param new_file_type: new file type
        :param new_file_state: new file state
        """
        print('quick_save_file_change_program_file_state', self.step, program.file_type, program.file_state, new_file_type, new_file_state)
        self.quick_save_file(program)
        self.change_program_file_state(
            program=program,
            new_file_type=new_file_type,
            new_file_state=new_file_state,
        )
        self.close_process(program)
        print('quick_save_file_change_program_file_state', self.step, program.file_type, program.file_state)
        
    def quick_save_file_load_from_game(self,
                                       program,
                                       ) -> None:
        """
        Quick save opened, actual file and load file from game
        :param program: Program object
        """
        print('quick_save_file_load_from_game', self.step, program.file_type, program.file_state)
        self.quick_save_file(program)
        self.load_from_game(program)
        print('quick_save_file_load_from_game end:', self.step, program.file_type, program.file_state)
        