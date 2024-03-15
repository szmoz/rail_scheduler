import pygame as pg

from code.util.background import Background
from code.util.event_manager import EventManager
from code.util.frame import Frame
from code.util.text import Text

from code.window.states import ButtonStates, ButtonEventStates
from code.window.variable_data import CustomEventTypes


class Window:
    """
    Window parent object
    Contains background, frame, topline, title, empty button dict, event manager for buttons
    """
    def __init__(self,
                 rect: pg.Rect,
                 background_color: tuple,
                 frame_thickness: int,
                 frame_top_color: tuple,
                 frame_bottom_color: tuple,
                 topline_height: int,
                 topline_color: tuple,
                 title_text: str,
                 title_color: tuple,
                 title_size: int,
                 title_type: str,
                 return_key_allowed: bool = True):
        """
        Initialize basic window object
        :param rect: rectangle area of window
        :param background_color: background color
        :param frame_thickness: frame thickness
        :param frame_top_color: top & left frame color
        :param frame_bottom_color: bottom & right frame color
        :param topline_height: topline height
        :param topline_color: topline color
        :param title_text: title
        :param title_color: title color
        :param title_size: title size
        :param title_type: title type (.ttf)
        :param return_key_allowed: True: Return key will click 0. button;False: no event action on Return key down
        """
        # Rect
        self.rect = rect
        # Topline
        self.topline = Background(
            rect=pg.Rect(
                self.rect.left + frame_thickness,
                self.rect.top + frame_thickness,
                self.rect.width - (frame_thickness * 2),
                topline_height
            ),
            color=topline_color
        )
        # Background
        self.background = Background(
            rect=pg.Rect(
                self.topline.rect.left,
                self.topline.rect.bottom,
                self.topline.rect.width,
                self.rect.height - (frame_thickness * 2) - self.topline.rect.height
            ),
            color=background_color
        )
        # Frame
        self.frame = Frame(
            rect=self.rect,
            thickness=frame_thickness,
            top_color=frame_top_color,
            bottom_color=frame_bottom_color,
        )
        # Title
        self.title = Text(
            text=title_text,
            text_type=title_type,
            size=title_size,
            color=title_color,
            anchor_type='midleft',
            anchor_pos=(
                self.topline.rect.left + self.frame.thickness,
                self.topline.rect.centery
            )
        )
        # Buttons
        self.buttons = dict()
        
        # Event management
        self.button_event_managers = {
            ButtonEventStates.STANDARD: EventManager(
                event_types=(pg.MOUSEBUTTONDOWN, pg.KEYDOWN),
                event_functions=(self.ispressed_start, self.keydown),
            ),
            ButtonEventStates.LEFT_MOUSE_PRESSED: EventManager(
                event_types=(pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.KEYDOWN),
                event_functions=(self.ispressed, self.isclicked, self.keydown),
            ),
        }
        
        # Dynamic variables
        self.button_state = ButtonEventStates.STANDARD
        self.button_pressed = -1
        self.button_clicked = -1
        self.return_key_allowed = return_key_allowed
        
    def button_event_manager(self,
                             event: pg.event.Event,
                             program,
                             ) -> bool:
        """
        Event manager for window buttons
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        return self.button_event_managers[self.button_state].handle(event=event, program=program)
    
    def ispressed(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        Check if mouse is pressing button when left mouse button pressed
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            # Button not pressed
            if self.button_pressed < 0:
                return False
            # Button pressed
            self.update_button(
                program=program,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
            self.button_pressed = -1
            return False
        # Collision
        # Same button
        if self.button_pressed == idx:
            return True
        # Different button
        if self.button_pressed >= 0:
            self.update_button(
                program=program,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
        self.button_pressed = idx
        self.update_button(
            program=program,
            button_idx=self.button_pressed,
            new_state=ButtonStates.PRESSED
        )
        return True
        
    def ispressed_start(self,
                        event: pg.event.Event,
                        program,
                        ) -> bool:
        """
        Check if mouse pressed button when left mouse button get pressed
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            return False
        # Collision
        self.button_state = ButtonEventStates.LEFT_MOUSE_PRESSED
        self.button_pressed = idx
        self.update_button(
            program=program,
            button_idx=self.button_pressed,
            new_state=ButtonStates.PRESSED,
        )
        return True
    
    def isclicked(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        Check if mouse clicked button
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            self.button_state = ButtonEventStates.STANDARD
            # Button not pressed
            if self.button_pressed < 0:
                return True
            # Button pressed
            self.update_button(
                program=program,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
            self.button_pressed = -1
            return True
        # Collision
        # Same button
        if self.button_pressed == idx:
            self.update_button(
                program=program,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
        # Different button
        else:
            self.button_pressed = idx
            self.update_button(
                program=program,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
        # Create button clicked event
        self.create_button_clicked_event(program, idx)
        program.break_event_loop = True
        return True
        
    def keydown(self,
                event: pg.event.Event,
                program,
                ) -> bool:
        """
        Check for Escape(close) and Return(OK) keys
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        if event.key == pg.K_ESCAPE:
            self.button_clicked = len(self.buttons) - 1
        elif event.key == pg.K_RETURN and self.return_key_allowed:
            self.button_clicked = 0
        if self.button_clicked < 0:
            return False
        # Create button clicked event
        self.create_button_clicked_event(program)
        return True
    
    def create_button_clicked_event(self,
                                    program,
                                    idx=None,
                                    ) -> None:
        """
        Create Custom windowbutton clicked event and post on queue
        :param program: Program object
        :param idx: index of clicked button
        """
        if idx is None:
            idx = self.button_clicked
        pg.event.post(pg.event.Event(
            CustomEventTypes.WINDOW_BUTTON_CLICKED,
            button_idx=idx
        ))
        program.break_event_loop = True
    
    def get_button_collision(self,
                             pos: tuple or list,
                             ) -> int:
        """
        Return colliding button's index
        :param pos: mouse position
        :return: -1: no collision 0...: colliding button's index
        """
        if not self.rect.collidepoint(pos):
            return -1
        for idx, button in self.buttons.items():
            if button.rect.collidepoint(pos):
                return idx
        return -1
    
    def update_button(self,
                      program,
                      button_idx: int,
                      new_state: int,
                      ) -> None:
        """
        Draw button
        :param program: Program object
        :param button_idx: index of button
        :param new_state: new button state
        """
        program.draw_rects.append(self.buttons[button_idx].update(
            surf_idx=new_state,
            surf=program.screen
        ))
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        pass
        
    def draw_basic(self,
                   surf: pg.Surface,
                   ) -> pg.Rect:
        """
        Draw basic window content on surface
        :param surf: surface
        """
        # Frame
        self.frame.draw(surf)
        # Topline
        self.topline.draw(surf)
        # Title
        self.title.draw(surf)
        # Background
        self.background.draw(surf)
        # Buttons
        for button in self.buttons.values():
            button.draw(surf)
        
        return self.rect
    
    def reposition(self,
                   new_screen_center: tuple,
                   ) -> None:
        pass
    
    def reposition_basic(self,
                         new_screen_center: tuple,
                         ) -> tuple:
        """
        Reposition window to display surface center when display is resized
        :param new_screen_center: new screen center
        :return (x_diff, y_diff)
        """
        x_diff = new_screen_center[0] - self.rect.centerx
        y_diff = new_screen_center[1] - self.rect.centery
        # Rect
        self.rect.x += x_diff
        self.rect.y += y_diff
        # Topline
        self.topline.rect.x += x_diff
        self.topline.rect.y += y_diff
        # Background
        self.background.rect.x += x_diff
        self.background.rect.y += y_diff
        # Frame
        for frame_sprite in self.frame.sprites():
            frame_sprite.rect.x += x_diff
            frame_sprite.rect.y += y_diff
        # Title
        self.title.rect.x += x_diff
        self.title.rect.y += y_diff
        # Buttons
        for button in self.buttons.values():
            button.rect.x += x_diff
            button.rect.y += y_diff
        return x_diff, y_diff
        