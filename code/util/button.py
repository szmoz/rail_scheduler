import pygame as pg

from code.util.frame import Frame
from code.util.text import Text


class Button:
    """
    Interactive button object
    Contains one Rect and at least one Surface
    Can be standard, pressed, mouse over
    If mouse over is possible, than pressed must be possible too
    """
    def __init__(self,
                 rect: pg.Rect,
                 background_color: tuple or list,
                 frame: bool = False,
                 frame_thickness: int = None,
                 frame_top_color: tuple or list = None,
                 frame_bottom_color: tuple or list = None,
                 frame_edge_lines: tuple or list = None,
                 text: str = None,
                 text_type: str = None,
                 text_size: int = None,
                 text_color: tuple or list = None,
                 pressed: bool = False,
                 frame_top_color_pressed: tuple or list = None,
                 frame_bottom_color_pressed: tuple or list = None,
                 background_color_pressed: tuple or list = None,
                 frame_edge_lines_pressed: tuple or list = None,
                 over: bool = False,
                 background_color_over: tuple or list = None,
                 frame_edge_lines_over: tuple or list = None,
                 ):
        """
        Initialize Button object
        :param rect: rectangle area where button will be drawn
        :param background_color: standard background color
        :param frame: True: button with frame; False: button without frame
        :param frame_thickness: frame thickness
        :param frame_top_color: top & left frame color
        :param frame_bottom_color: bottom & right frame color
        :param text: text on button
        :param text_type: path to text type
        :param text_size: size of text
        :param text_color: color of text
        :param pressed: True: button can be pressed; False button cannot be pressed
        :param frame_top_color_pressed: top & left frame color when button is pressed
        :param frame_bottom_color_pressed: bottom & right frame color when button is pressed
        :param background_color_pressed: background color when button is pressed
        :param over: True: button has different background when mouse is over button
        :param background_color_over: background color when mouse is over button
        """
        # Rect
        self.rect = rect
        # Surfaces
        surf_count = 1
        if pressed:
            surf_count += 1
        if over:
            surf_count += 1
        self.surfs = []
        for i in range(surf_count):
            self.surfs.append(pg.Surface(self.rect.size))
        
        # Surface content
        # Background
        backgrounds = (background_color, background_color_pressed, background_color_over)
        for i in range(surf_count):
            self.surfs[i].fill(backgrounds[i])
        # Frame
        if frame:
            frames = [Frame(
                rect=pg.Rect(
                    (0, 0),
                    self.rect.size
                ),
                thickness=frame_thickness,
                top_color=frame_top_color,
                bottom_color=frame_bottom_color,
                edge_lines=frame_edge_lines
            )]
            if pressed:
                frames.append(Frame(
                    rect=pg.Rect(
                        (0, 0),
                        self.rect.size
                    ),
                    thickness=frame_thickness,
                    top_color=frame_top_color_pressed,
                    bottom_color=frame_bottom_color_pressed,
                    pressed=pressed,
                    edge_lines=frame_edge_lines_pressed
                ))
            if over:
                frames.append(Frame(
                    rect=pg.Rect(
                        (0, 0),
                        self.rect.size
                    ),
                    thickness=frame_thickness,
                    top_color=frame_top_color,
                    bottom_color=frame_bottom_color,
                    edge_lines=frame_edge_lines_over
                ))
            for i in range(surf_count):
                frames[i].draw(self.surfs[i])
        # Text
        if text is not None:
            texts = [Text(
                text=text,
                text_type=text_type,
                size=text_size,
                color=text_color,
                anchor_type='center',
                anchor_pos=(self.rect.width // 2, self.rect.height // 2)
            )]
            if pressed:
                texts.append(Text(
                    text=text,
                    text_type=text_type,
                    size=text_size,
                    color=text_color,
                    anchor_type='center',
                    anchor_pos=(self.rect.width // 2 + (frame_thickness // 2),
                                self.rect.height // 2 + (frame_thickness // 2))
                ))
            if over:
                texts.append(texts[0])
            for i in range(surf_count):
                texts[i].draw(self.surfs[i])
        
        # Dynamic variables
        self.actual = 0
                
    def draw(self,
             surf: pg.Surface):
        """
        Draw button onto surface
        :param surf: Surface
        """
        surf.blit(self.surfs[self.actual], self.rect)
        
    def update(self,
               surf_idx: int,
               surf: pg.Surface):
        """
        Change button surface and redraw
        :param surf_idx: 0:standard; 1:pressed; 2:over
        :param surf: surface
        """
        self.actual = surf_idx
        self.draw(surf)
    