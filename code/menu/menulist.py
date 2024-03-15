import pygame as pg

from code.menu.states import MenuStates

from code.util.event_manager import EventManager
from code.util.frame import Frame
from code.util.text import Text


class Menulist:
    """
    Dropdown list in menu
    """
    def __init__(self,
                 topleft: tuple or list,
                 background_color: tuple or list,
                 background_color_over: tuple or list,
                 frame_thickness: int,
                 frame_top_color: tuple or list,
                 frame_bottom_color: tuple or list,
                 texts: list,
                 text_type: str,
                 text_size: int,
                 text_color: tuple or list,
                 ) -> None:
        """
        Initialize MenuList object
        :param topleft: topleft position of object
        :param background_color: background color
        :param background_color_over: background color of element when mouse is over
        :param frame_thickness: frame thickness
        :param frame_top_color: frame top & left color
        :param frame_bottom_color: frame bottom & right color
        :param texts: list of texts
        :param text_type: path to '.ttf' file
        :param text_size: size of text
        :param text_color: color of text
        """
        # Data
        self.background_color = background_color
        self.background_color_over = background_color_over
        
        # Surface content
        # Texts
        self.texts = dict()
        for i in range(len(texts)):
            self.texts[i] = Text(
                text=texts[i],
                text_type=text_type,
                size=text_size,
                color=text_color,
                anchor_type='midleft',
                anchor_pos=(0, 0)
            )
        max_width = 0
        max_height = 0
        for text in self.texts.values():
            if text.rect.width > max_width:
                max_width = text.rect.width
            if text.rect.height > max_height:
                max_height = text.rect.height
        element_size = (
            max_width + 5,
            max_height + 4,
        )
        # Rect
        self.rect = pg.Rect(
            topleft[0],
            topleft[1],
            element_size[0] + (frame_thickness * 2),
            element_size[1] * len(self.texts) + (frame_thickness * 2)
        )
        self.element_rects = dict()
        act_top = self.rect.top + frame_thickness
        for i in range(len(self.texts)):
            self.element_rects[i] = pg.Rect(
                (self.rect.left + frame_thickness,
                 act_top),
                element_size
            )
            act_top += element_size[1]
        # Text rect update
        for idx, text in self.texts.items():
            text.change_anchor_pos(
                new_anchor_pos=(
                    self.element_rects[idx].left + frame_thickness,
                    self.element_rects[idx].centery
                )
            )
        # Frame
        self.frame = Frame(
            rect=self.rect,
            thickness=frame_thickness,
            top_color=frame_top_color,
            bottom_color=frame_bottom_color,
        )
        
        # Event management
        self.event_manager = EventManager(
            event_types=(pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN),
            event_functions=(self.isover, self.isclicked)
        )
        
        # Dynamic variables
        self.element_over = -1
        
    def isclicked(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        Check if element is clicked when mousebutton down
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event (+event_loop breaker); False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_element_collision(event.pos)
        # No collision
        if idx < 0:
            # Element not over
            if self.element_over < 0:
                return False
            # Element over
            self.element_over = -1
            program.redraw = True
            return False
        # Collision
        # Inactive element
        # Active element
        menubar_button_idx = program.menu.menubar.button_pressed
        list_element_idx = self.element_over
        # Reset menu
        self.element_over = -1
        program.menu.menubar.close_menu_with_esc(event=pg.event.Event(
            pg.KEYDOWN,
            key=pg.K_ESCAPE
        ), program=program)
        # Start menu process action
        program.menu.process.start_new_action(menubar_button_idx=menubar_button_idx, list_element_idx=list_element_idx,
                                              program=program)
        return True
        
    def isover(self,
               event: pg.event.Event,
               program,
               ) -> bool:
        """
        Check if mouse is over any element
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Get colliding button index
        idx = self.get_element_collision(event.pos)
        # No collision
        if idx < 0:
            # Element not over
            if self.element_over < 0:
                return False
            # Element over
            self.element_over = -1
            program.redraw = True
            return True
        # Collision
        # Element not over
        if self.element_over < 0:
            self.element_over = idx
            self.update_elements(program)
            return True
        # Element over
        # Same button
        if self.element_over == idx:
            return True
        # Different button
        self.element_over = idx
        program.redraw = True
        return True
        
    def update_elements(self,
                        program,
                        ) -> None:
        """
        Redraw elements
        :param program: Program object
        """
        program.draw_rects.append(self.draw(program.screen))
        
    def get_element_collision(self,
                              pos: tuple or list,
                              ) -> int:
        """
        Return colliding element's index
        :param pos: mouse position
        :return: -1: no collision 0...: colliding element's index
        """
        if not self.rect.collidepoint(pos):
            return -1
        for idx, element_rect in self.element_rects.items():
            if element_rect.collidepoint(pos):
                return idx
        return -1
    
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw menulist on surface
        :param surf: Surface
        :return rect area to draw
        """
        # Background
        pg.draw.rect(
            surface=surf,
            color=self.background_color,
            rect=self.rect
        )
        # Over element
        if self.element_over >= 0:
            pg.draw.rect(
                surface=surf,
                color=self.background_color_over,
                rect=self.element_rects[self.element_over]
            )
        # Frame
        self.frame.draw(surf)
        # Texts
        for text in self.texts.values():
            text.draw(surf)
        return self.rect
    