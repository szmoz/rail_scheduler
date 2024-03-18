import math
import pygame as pg

from code.util.button import Button
from code.util.text import Text

from code.window.color_data import AskColors as Colors
from code.window.color_data import Colors as WinColors
from code.window.size_data import AskWinSizes as Sizes
from code.window.size_data import Sizes as WinSizes
from code.window.string_data import AskStrings as Strings
from code.window.string_data import Strings as WinStrings
from code.window.window import Window


class ErrorWindow(Window):
    """
    Window with error message and OK button
    """
    def __init__(self,
                 win_type: int,
                 error_message: str,
                 screen_center: tuple,
                 ) -> None:
        """
        Initialize Error window
        :param win_type: type code of window
        :param error_message: error message to appear in error window
        :param screen_center: display screen's center
        """
        # Data
        self.type = win_type
        # Surface content
        # Error message
        self.message = [Text(
            text=error_message,
            text_type=Strings.QUESTION_TYPE,
            size=Sizes.QUESTION,
            color=Colors.QUESTION,
            anchor_type="center",
            anchor_pos=screen_center
        )]
        # Breaking text
        if self.message[0].rect.width > Sizes.MAX_WIDTH - (WinSizes.FRAME_THICKNESS * 8):
            print('itt')
            break_point = len(error_message) // 2
            act_idx = len(error_message) // 2
            diff = 1
            for i in range(len(error_message)):
                print(act_idx)
                if error_message[act_idx] == " ":
                    print('act_idx', act_idx)
                    break_point = act_idx
                    break
                act_idx += diff
                diff *= -1
                diff += int(math.copysign(1, diff))
            rect_height = self.message[0].rect.height
            self.message.clear()
            self.message.append(Text(
                text=error_message[:break_point],
                text_type=Strings.QUESTION_TYPE,
                size=Sizes.QUESTION,
                color=Colors.QUESTION,
                anchor_type="center",
                anchor_pos=(screen_center[0], screen_center[1] - rect_height // 2)
            ))
            self.message.append(Text(
                text=error_message[break_point + 1:],
                text_type=Strings.QUESTION_TYPE,
                size=Sizes.QUESTION,
                color=Colors.QUESTION,
                anchor_type="center",
                anchor_pos=(screen_center[0], screen_center[1] + rect_height // 2)
            ))
        # Rect
        message_width = 0
        for line in self.message:
            if line.rect.width > message_width:
                question_width = line.rect.width
        rect_width = max(message_width + (WinSizes.FRAME_THICKNESS * 8), Sizes.MIN_WIDTH)
        rect_width = min(rect_width, Sizes.MAX_WIDTH)
        rect_height = (len(self.message) * self.message[0].rect.height) + \
                      (Sizes.BUTTON_HEIGHT * 3) + \
                      (WinSizes.FRAME_THICKNESS * 2) + WinSizes.TOPLINE_HEIGHT
        self.rect = pg.Rect(
            screen_center[0] - (rect_width // 2),
            screen_center[1] - (rect_height // 2),
            rect_width,
            rect_height
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
            title_text="Error",
            title_color=WinColors.TITLE,
            title_size=WinSizes.TITLE,
            title_type=WinStrings.TITLE_TYPE,
        )
        # Button
        self.buttons[0] = Button(
            rect=pg.Rect(
                self.rect.centerx - (Sizes.BUTTON_WIDTH // 2),
                self.rect.bottom - self.frame.thickness - int(Sizes.BUTTON_HEIGHT * 1.5),
                Sizes.BUTTON_WIDTH,
                Sizes.BUTTON_HEIGHT
            ),
            background_color=WinColors.BUTTON_BACKGROUND,
            frame=True,
            frame_thickness=Sizes.BUTTON_FRAME_THICKNESS,
            frame_top_color=WinColors.BUTTON_FRAME_TOP,
            frame_bottom_color=WinColors.BUTTON_FRAME_BOTTOM,
            text="OK",
            text_type=Strings.BUTTON_TYPE,
            text_size=Sizes.BUTTON_TEXT,
            text_color=WinColors.BUTTON_TEXT,
            pressed=True,
            frame_top_color_pressed=WinColors.BUTTON_FRAME_TOP_PRESSED,
            frame_bottom_color_pressed=WinColors.BUTTON_FRAME_BOTTOM_PRESSED,
            background_color_pressed=WinColors.BUTTON_BACKGROUND_PRESSED,
            frame_edge_lines_pressed=(3, 4),
        )
    
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for error message window
        :param event: pygame Event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        return self.button_event_manager(
            event=event,
            program=program)
    
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        # Basic content
        self.draw_basic(surf)
        # Message
        for message in self.message:
            message.draw(surf)
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
        # Message
        for message in self.message:
            message.rect.x += x_diff
            message.rect.y += y_diff
        