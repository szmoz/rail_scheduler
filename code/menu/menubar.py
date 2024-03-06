import pygame as pg

from code.util.background import BackgroundResizable
from code.util.button import Button


class MenuBar:
    """
    Menu bar with menu buttons and resizable background
    Buttons stay at topleft position always
    """
    def __init__(self,
                 rect: pg.Rect,
                 background_color: tuple or list,
                 button_width: int,
                 button_background_color: tuple or list,
                 button_background_color_pressed: tuple or list,
                 button_background_color_over: tuple or list,
                 button_frame_thickness: int,
                 button_frame_top_color: tuple or list,
                 button_frame_bottom_color: tuple or list,
                 button_frame_edge_lines: tuple or list,
                 button_frame_top_color_pressed: tuple or list,
                 button_frame_bottom_color_pressed: tuple or list,
                 button_frame_edge_lines_pressed: tuple or list,
                 button_frame_edge_lines_over: tuple or list,
                 button_texts: tuple or list,
                 text_type: str,
                 text_size: int,
                 text_color: tuple or list,
                 ):
        """
        Initialize MenuBar object
        :param rect: rectangle area of menubar
        :param background_color: background color
        :param button_width: minimum button width
        :param button_background_color: button background color
        :param button_background_color_pressed: button background color when button is pressed
        :param button_background_color_over: button background color when mouse is over button
        :param button_frame_thickness: button frame thickness
        :param button_frame_top_color: button frame top & left color
        :param button_frame_bottom_color: button frame bottom & right color
        :param button_frame_edge_lines: list of standard button frame edge lines
        :param button_frame_top_color_pressed: button frame top & left color when button is pressed
        :param button_frame_bottom_color_pressed: button frame bottom & right color when button is pressed
        :param button_frame_edge_lines_pressed: list of pressed button frame edge lines
        :param button_frame_edge_lines_over: list of mouse-over button frame edge lines
        :param button_texts: list of button texts
        :param text_type: path to '.ttf' file
        :param text_size: size of text
        :param text_color: color of text
        """
        # Rect
        self.rect = rect
        
        # Surface content
        # Background
        self.background = BackgroundResizable(
            rect=self.rect,
            color=background_color
        )
        # Buttons
        self.buttons = dict()
        prev_left = self.rect.left
        for i in range(len(button_texts)):
            self.buttons[i] = Button(
                rect=pg.Rect(
                    prev_left,
                    self.rect.top,
                    button_width,
                    self.rect.height
                ),
                background_color=button_background_color,
                frame=True,
                frame_thickness=button_frame_thickness,
                frame_top_color=button_frame_top_color,
                frame_bottom_color=button_frame_bottom_color,
                frame_edge_lines=button_frame_edge_lines[i],
                text=button_texts[i],
                text_type=text_type,
                text_size=text_size,
                text_color=text_color,
                pressed=True,
                frame_top_color_pressed=button_frame_top_color_pressed,
                frame_bottom_color_pressed=button_frame_bottom_color_pressed,
                background_color_pressed=button_background_color_pressed,
                frame_edge_lines_pressed=button_frame_edge_lines_pressed[i],
                over=True,
                background_color_over=button_background_color_over,
                frame_edge_lines_over=button_frame_edge_lines_over[i]
            )
            prev_left += button_width
            
        # Event managers
        
        
        # Dynamic variables
        self.buttons_to_draw = []
        
    def button_to_draw(self,
                       button_idx: int):
        """
        Prepare a button for redraw
        :param button_idx: index of button that needs redraw
        """
        self.buttons_to_draw.append(button_idx)
        
    def on_draw(self,
                surf: pg.Surface,
                ) -> list:
        """
        Draw only buttons that need redraw
        :param surf: surface
        :return list of rect areas to draw
        """
        draw_rects = []
        for button_idx in self.buttons_to_draw:
            self.buttons[button_idx].draw(surf)
            draw_rects.append(self.buttons[button_idx].rect)
        self.buttons_to_draw.clear()
        return draw_rects
        
    def on_redraw(self,
                  surf: pg.Surface,
                  ) -> pg.Rect:
        """
        Draw menubar content on surface
        :param surf: surface
        :return rect area to draw
        """
        # Background
        self.background.draw(surf)
        # Buttons
        for button in self.buttons.values():
            button.draw(surf)
        return self.rect
            
    def change_size(self,
                    new_size: tuple or list):
        """
        Resize menubar's background
        Buttons stay at original position
        :param new_size: new size
        """
        # Rect
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
        # Background
        self.background.change_size(new_size)
        
        
class ButtonStates:
    STANDARD = 0
    PRESSED = 1
    OVER = 2
    