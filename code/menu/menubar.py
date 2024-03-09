import pygame as pg

from code.game.states import GameSates

from code.menu.states import MenuStates, MenubarStates

from code.util.background import BackgroundResizable
from code.util.button import Button
from code.util.event_manager import EventManager


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
                 ) -> None:
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
        self.event_managers = {
            MenubarStates.STANDARD: EventManager(
                event_types=(pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN),
                event_functions=(self.isover, self.ispressed_start),
            ),
            MenubarStates.LEFT_MOUSE_PRESSED: EventManager(
                event_types=(pg.MOUSEMOTION, pg.MOUSEBUTTONUP),
                event_functions=(self.ispressed, self.isclicked),
            ),
            MenubarStates.MENU_OPENED: EventManager(
                event_types=(pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN),
                event_functions=(self.isover_menu_opened, self.ispressed_opened)
            ),
        }
        
        # Dynamic variables
        self.state = MenubarStates.STANDARD
        self.button_over = -1
        self.button_pressed = -1
        
    def event_manager(self,
                      event: pg.event.Event,
                      game,
                      ) -> bool:
        """
        Event manager for menubar
        :param event: pygame event
        :param game: Game object
        :return: True: go to next event; False: go to next event manager
        """
        return self.event_managers[self.state].handle(
            event=event,
            game=game,
        )
        
    def open_menu(self,
                  game,
                  ) -> bool:
        """
        Open menu
        Change menu and menubar states to opened, set opened list index
        :param game: Game object
        :return: True: go to next event
        """
        self.state = MenubarStates.MENU_OPENED
        game.menu.state = MenuStates.OPENED
        game.menu.list_opened = self.button_pressed
        game.state = GameSates.OPENED_MENU
        game.redraw = True
        return True
    
    def close_menu(self,
                   game,
                   ) -> bool:
        """
        Close menu
        Change menu and menubar states to closed/standard
        :param game: Game object
        :return: True: go to next event (+event_loop breaker)
        """
        self.state = MenubarStates.STANDARD
        game.menu.state = MenuStates.CLOSED
        game.menu.list_opened = -1
        game.state = game.isopened
        game.redraw = True
        game.break_event_loop = True
        return True
    
    def close_menu_with_esc(self,
                            event: pg.event.Event,
                            game,
                            ) -> bool:
        """
        Close menu with Escape key
        :param event: pygame event
        :param game: Game object
        :return: True: go to next event (+event_loop breaker)
        """
        if event.key != pg.K_ESCAPE:
            return False
        button_idx = self.get_button_collision(pos=pg.mouse.get_pos())
        new_state = ButtonStates.STANDARD
        if button_idx >= 0:
            new_state = ButtonStates.OVER
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=new_state
        )
        self.button_pressed = -1
        self.button_over = button_idx
        return self.close_menu(game)
    
    def isclicked(self,
                  event: pg.event.Event,
                  game,
                  ) -> bool:
        """
        Check if button is clicked when mousebutton up
        :param event: pygame event
        :param game: Game object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            self.state = MenubarStates.STANDARD
            # Button not pressed
            if self.button_pressed < 0:
                return True
            # Button pressed
            self.update_button(
                game=game,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
            self.button_pressed = -1
            return True
        # Collision
        # Different button
        if self.button_pressed != idx:
            if self.button_pressed >= 0:
                self.update_button(
                    game=game,
                    button_idx=self.button_pressed,
                    new_state=ButtonStates.STANDARD
                )
            self.button_pressed = idx
            self.update_button(
                game=game,
                button_idx=self.button_pressed,
                new_state=ButtonStates.PRESSED
            )
        # Same button
        return self.open_menu(game)
        
    def ispressed(self,
                  event: pg.event.Event,
                  game,
                  ) -> bool:
        """
        Check if button is pressed when mousemotion
        :param event: pygame event
        :param game: Game object
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
                game=game,
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
                game=game,
                button_idx=self.button_pressed,
                new_state=ButtonStates.STANDARD
            )
        self.button_pressed = idx
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=ButtonStates.PRESSED
        )
        return True

    def ispressed_start(self,
                        event: pg.event.Event,
                        game,
                        ) -> bool:
        """
        Check if button is pressed when left mousebutton down
        :param event: pygame event
        :param game: Game object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            # Button not over
            if self.button_over < 0:
                return False
            # Button over
            self.update_button(
                game=game,
                button_idx=self.button_over,
                new_state=ButtonStates.STANDARD
            )
            self.button_over = -1
            return False
        # Collision
        self.state = MenubarStates.LEFT_MOUSE_PRESSED
        # Button not over
        if self.button_over < 0:
            self.button_pressed = idx
            self.update_button(
                game=game,
                button_idx=self.button_pressed,
                new_state=ButtonStates.PRESSED
            )
            return True
        # Button over
        if self.button_over != idx:
            self.update_button(
                game=game,
                button_idx=self.button_over,
                new_state=ButtonStates.STANDARD
            )
        self.button_over = -1
        self.button_pressed = idx
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=ButtonStates.PRESSED
        )
        return True
    
    def ispressed_opened(self,
                         event: pg.event.Event,
                         game,
                         ) -> bool:
        """
        Check for button press when menubar is opened
        :param event: pygame event
        :param game: Game object
        :return: True:go to next event; False:go to next event manager
        """
        if event.button != pg.BUTTON_LEFT:
            return False
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            return False
        # Collision
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=ButtonStates.OVER
        )
        self.button_pressed = -1
        self.button_over = idx
        return self.close_menu(game)
    
    def isover_menu_opened(self,
                           event: pg.event.Event,
                           game,
                           ) -> bool:
        """
        Check if mouse is over any button when menu is open
        :param event: pygame event
        :param game: Game object
        :return: True:go to next event; False:go to next event manager
        """
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            return False
        # Collision
        # Same button
        if self.button_pressed == idx:
            return True
        # Different button
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=ButtonStates.STANDARD
        )
        self.button_pressed = idx
        self.update_button(
            game=game,
            button_idx=self.button_pressed,
            new_state=ButtonStates.PRESSED
        )
        # Action
        return self.open_menu(game)
        
    def isover(self,
               event: pg.event.Event,
               game,
               ) -> bool:
        """
        Check if mouse is over any button
        :param event: pygame event
        :param game: Game object
        :return: True:go to next event; False:go to next event manager
        """
        # Get colliding button index
        idx = self.get_button_collision(event.pos)
        # No collision
        if idx < 0:
            # Button not over
            if self.button_over < 0:
                return False
            # Button over
            self.update_button(
                game=game,
                button_idx=self.button_over,
                new_state=ButtonStates.STANDARD
            )
            self.button_over = -1
            return True
        # Collision
        # Button not over
        if self.button_over < 0:
            self.button_over = idx
            self.update_button(
                game=game,
                button_idx=self.button_over,
                new_state=ButtonStates.OVER
            )
            return True
        # Button over
        # Same button
        if self.button_over == idx:
            return True
        # Different button
        self.update_button(
            game=game,
            button_idx=self.button_over,
            new_state=ButtonStates.STANDARD
        )
        self.button_over = idx
        self.update_button(
            game=game,
            button_idx=self.button_over,
            new_state=ButtonStates.OVER
        )
        return True
    
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
                      game,
                      button_idx: int,
                      new_state: int,
                      ):
        """
        Draw button
        :param game: Game object
        :param button_idx: index of button
        :param new_state: new button state
        """
        game.draw_rects.append(self.buttons[button_idx].update(
            surf_idx=new_state,
            surf=game.screen
        ))
        
    def draw(self,
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
    