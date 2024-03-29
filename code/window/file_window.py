import pygame as pg

from code.util.button import Button
from code.util.textbox import FileWinTextBox

from code.window.color_data import FileColors as Colors
from code.window.color_data import Colors as WinColors
from code.window.file_name_list import FileNameList
from code.window.size_data import FileWinSizes as Sizes
from code.window.size_data import Sizes as WinSizes
from code.window.string_data import FileStrings as Strings
from code.window.string_data import Strings as WinStrings
from code.window.variable_data import FileWinFrameEdges as FrameEdges
from code.window.window import Window


class FileWindow(Window):
    """
    Window with file list, textbox and 2+1 buttons
    """
    def __init__(self,
                 win_type: int,
                 file_type: int,
                 screen_center: tuple,
                 title: str,
                 start_text: str = None,
                 ) -> None:
        """
        Initialize File window
        :param win_type:  type code of window
        :param file_type: type code of file
        :param screen_center: display screen's center
        :param title: title text
        :param start_text: file name to appear in textbox at startup
        """
        # Data
        self.win_type = win_type
        self.file_type = file_type
        # Surface content
        # Rect
        self.rect = pg.Rect(
            screen_center[0] - (Sizes.WIDTH // 2),
            screen_center[1] - (Sizes.HEIGHT // 2),
            Sizes.WIDTH,
            Sizes.HEIGHT
        )
        # Basic content
        super().__init__(
            rect=self.rect,
            background_color=WinColors.BACKGROUND,
            frame_thickness=WinSizes.FRAME_THICKNESS,
            frame_top_color=WinColors.FRAME_TOP,
            frame_bottom_color=WinColors.FRAME_BOTTOM,
            topline_height=WinSizes.TOPLINE_HEIGHT,
            topline_color=WinColors.TOPLINE,
            title_text=title,
            title_color=WinColors.TITLE,
            title_size=WinSizes.TITLE,
            title_type=WinStrings.TITLE_TYPE,
        )
        # Buttons
        button_left = self.rect.right - self.frame.thickness - int(Sizes.BUTTON_WIDTH * 1.5)
        button_top = self.rect.bottom - self.frame.thickness - (Sizes.BUTTON_HEIGHT * 2)
        for i in range(1, -1, -1):
            self.buttons[i] = Button(
                rect=pg.Rect(
                    button_left,
                    button_top,
                    Sizes.BUTTON_WIDTH,
                    Sizes.BUTTON_HEIGHT
                ),
                background_color=WinColors.BUTTON_BACKGROUND,
                frame=True,
                frame_thickness=Sizes.BUTTON_FRAME_THICKNESS,
                frame_top_color=WinColors.BUTTON_FRAME_TOP,
                frame_bottom_color=WinColors.BUTTON_FRAME_BOTTOM,
                text=Strings.BUTTON_TEXTS[win_type][i],
                text_type=Strings.BUTTON_TYPE,
                text_size=Sizes.BUTTON_TEXT,
                text_color=WinColors.BUTTON_TEXT,
                pressed=True,
                frame_top_color_pressed=WinColors.BUTTON_FRAME_TOP_PRESSED,
                frame_bottom_color_pressed=WinColors.BUTTON_FRAME_BOTTOM_PRESSED,
                background_color_pressed=WinColors.BUTTON_BACKGROUND_PRESSED,
                frame_edge_lines_pressed=FrameEdges.BUTTON_PRESSED,
            )
            button_top -= int(Sizes.BUTTON_HEIGHT * 1.5)
        # Corner button
        self.buttons[2] = Button(
            rect=pg.Rect(
                self.topline.rect.right - WinSizes.CORNER_BUTTON_GAP - WinSizes.CORNER_BUTTON_SIZE,
                self.topline.rect.top + WinSizes.CORNER_BUTTON_GAP,
                WinSizes.CORNER_BUTTON_SIZE,
                WinSizes.CORNER_BUTTON_SIZE
            ),
            background_color=WinColors.BUTTON_BACKGROUND,
            frame=True,
            frame_thickness=Sizes.BUTTON_FRAME_THICKNESS,
            frame_top_color=WinColors.BUTTON_FRAME_TOP,
            frame_bottom_color=WinColors.BUTTON_FRAME_BOTTOM,
            text="",
            text_type=Strings.BUTTON_TYPE,
            text_size=Sizes.BUTTON_TEXT,
            text_color=WinColors.BUTTON_TEXT,
            pressed=True,
            frame_top_color_pressed=WinColors.BUTTON_FRAME_TOP_PRESSED,
            frame_bottom_color_pressed=WinColors.BUTTON_FRAME_BOTTOM_PRESSED,
            background_color_pressed=WinColors.BUTTON_BACKGROUND_PRESSED,
            image_path='resources/graphics/corner_button.png',
        )
        # Textbox
        self.textbox = FileWinTextBox(
            rect=pg.Rect(
                self.topline.rect.left + int(Sizes.BUTTON_WIDTH * 0.25),
                button_top + int(Sizes.BUTTON_HEIGHT * 1.5),
                button_left - self.topline.rect.left - int(Sizes.BUTTON_WIDTH * 4.2),
                Sizes.TEXTBOX_HEIGHT
            ),
            frame_thickness=Sizes.TEXTBOX_FRAME_THICKNESS,
            frame_top_color=Colors.TEXTBOX_FRAME_TOP,
            frame_bottom_color=Colors.TEXTBOX_FRAME_BOTTOM,
            frame_edge_lines=FrameEdges.TEXTBOX,
            text_size=Sizes.TEXTBOX_TEXT,
            text_type=Strings.TEXTBOX_TYPE,
            align="left",
            start_text=start_text,
        )
        # List
        self.list = FileNameList(
            rect=pg.Rect(
                self.topline.rect.left + int(Sizes.BUTTON_WIDTH * 0.25),
                self.topline.rect.bottom + self.topline.rect.height,
                self.topline.rect.width - int(Sizes.BUTTON_WIDTH * 0.5),
                (self.textbox.rect.top - Sizes.BUTTON_HEIGHT) - (self.topline.rect.bottom + self.topline.rect.height),
            ),
            frame_thickness=Sizes.LIST_FRAME_THICKNESS,
            frame_top_color=Colors.LIST_FRAME_TOP,
            frame_bottom_color=Colors.LIST_FRAME_BOTTOM,
            frame_edge_lines=FrameEdges.LIST,
            text_size=Sizes.LIST_TEXT,
            text_type=Strings.LIST_TYPE,
            file_type=self.file_type,
        )
        
        # Event management
        self.event_managers = (
            self.textbox.event_manager,
            self.list.event_manager,
        )
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for ask window
        :param event: pygame Event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        for event_manager in self.event_managers:
            if event_manager(
                    event=event,
                    program=program,
                    file_win=self):
                return True
            if program.break_event_loop:
                return True
        if self.button_event_manager(
                event=event,
                program=program):
            return True
        return False
    
    def is_file_name_exist(self):
        """
        Check if textbox text is a name of an existing file in directory
        :return: True: file is in dir; False: file is not in dir
        """
        if self.list.find_name(self.textbox.text.text) < 0:
            return False
        return True
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw File Window on surface
        :param surf: surface
        :return: rectangle area for program.draw_rect
        """
        # Basic content
        self.draw_basic(surf)
        # List
        self.list.draw(surf)
        # Textbox
        self.textbox.draw(surf)
        return self.rect
        
    def reposition(self,
                   new_screen_center: tuple,
                   ) -> None:
        """
        Reposition window to display surface center when display is resized
        :param new_screen_center: new screen center
        """
        # Basic content
        x_diff, y_diff = self.reposition_basic(new_screen_center)
        # List
        self.list.reposition(x_diff, y_diff)
        # Textbox
        self.textbox.reposition(x_diff, y_diff)
        