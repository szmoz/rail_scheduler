import pygame as pg

from code.util.button import Button

from code.window.color_data import FileColors as Colors
from code.window.color_data import Colors as WinColors
from code.window.size_data import FileWinSizes as Sizes
from code.window.size_data import Sizes as WinSizes
from code.window.string_data import FileStrings as Strings
from code.window.string_data import Strings as WinStrings
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
                 start_text: str = '',
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
        self.type = win_type
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
        # List ------------------------------------------------------------
        # Textbox
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
                frame_edge_lines_pressed=(3, 4),
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
        
        self.event_managers = (
            self.button_event_manager,  # need to add list and textbox event managers
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
            if program.break_event_loop:
                return True
            if event_manager(
                    event=event,
                    program=program,):
                return True
        return False
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        # Basic content
        self.draw_basic(surf)
        # List ------------------------------------------------------------
        # Textbox
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
        # List ------------------------------------------------------------
        # Textbox
        