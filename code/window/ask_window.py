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


class AskWindow(Window):
    """
    Window with question and 3+1 buttons
    """
    def __init__(self,
                 win_type: int,
                 screen_center: tuple,
                 question: str,
                 ) -> None:
        """
        Initialize Ask window
        :param win_type: type code of window
        :param screen_center: display screen's center
        :param question: question to appear in ask window
        """
        # Data
        self.type = win_type
        # Surface content
        # Question
        self.question = [Text(
            text=question,
            text_type=Strings.QUESTION_TYPE,
            size=Sizes.QUESTION,
            color=Colors.QUESTION,
            anchor_type="center",
            anchor_pos=screen_center
        )]
        # Breaking text
        if self.question[0].rect.width > Sizes.MAX_WIDTH - (WinSizes.FRAME_THICKNESS * 8):
            print('itt')
            break_point = len(question) // 2
            act_idx = len(question) // 2
            diff = 1
            for i in range(len(question)):
                print(act_idx)
                if question[act_idx] == " ":
                    print('act_idx', act_idx)
                    break_point = act_idx
                    break
                act_idx += diff
                diff *= -1
                diff += int(math.copysign(1, diff))
            rect_height = self.question[0].rect.height
            self.question.clear()
            self.question.append(Text(
                text=question[:break_point],
                text_type=Strings.QUESTION_TYPE,
                size=Sizes.QUESTION,
                color=Colors.QUESTION,
                anchor_type="center",
                anchor_pos=(screen_center[0], screen_center[1] - rect_height // 2)
            ))
            self.question.append(Text(
                text=question[break_point + 1:],
                text_type=Strings.QUESTION_TYPE,
                size=Sizes.QUESTION,
                color=Colors.QUESTION,
                anchor_type="center",
                anchor_pos=(screen_center[0], screen_center[1] + rect_height // 2)
            ))
            
        # Rect
        question_width = 0
        for line in self.question:
            if line.rect.width > question_width:
                question_width = line.rect.width
        rect_width = max(question_width + (WinSizes.FRAME_THICKNESS * 8), Sizes.MIN_WIDTH)
        rect_width = min(rect_width, Sizes.MAX_WIDTH)
        rect_height = (len(self.question) * self.question[0].rect.height) + \
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
            title_text="",
            title_color=WinColors.TITLE,
            title_size=WinSizes.TITLE,
            title_type=WinStrings.TITLE_TYPE,
        )

        # Buttons
        button_left = self.rect.centerx - (Sizes.BUTTON_WIDTH * 2)
        button_top = self.rect.bottom - self.frame.thickness - int(Sizes.BUTTON_HEIGHT * 1.5)
        for i in range(3):
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
            button_left += int(Sizes.BUTTON_WIDTH * 1.5)
        # Corner button
        self.buttons[3] = Button(
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
        return self.button_event_manager(
            event=event,
            program=program)
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        # Basic content
        self.draw_basic(surf)
        # Question
        for question in self.question:
            question.draw(surf)
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
        # Question
        for question in self.question:
            question.rect.x += x_diff
            question.rect.y += y_diff
            