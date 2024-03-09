import pygame
import pygame as pg
import sys

from code.camera.camera import Camera

from code.game.color_data import Colors as C
from code.game.size_data import Sizes as S
from code.game.states import GameSates
from code.game.string_data import Strings as GameStrings
import code.game.variable_data as v

from code.menu.menu import Menu

from code.toolbar.toolbar import Toolbar

from code.util.event_manager import EventManager
from code.util.frame import FrameResizable


class Game:
    """
    Main object of program
    Contains every object of program
    After initialization the 'run' function runs until the program is shut down
    """
    def __init__(self) -> None:
        """
        Create Game object and run game
        """
        print(pg.USEREVENT)
        print(pg.NUMEVENTS - 1)
        # Data
        self.screen_width = S.SCREEN_WIDTH
        self.screen_height = S.SCREEN_HEIGHT
        self.screen_size = (self.screen_width, self.screen_height)
        self.min_screen_size = self.screen_size

        # Icon
        self.icon = pg.image.load("resources/graphics/icon.png")
        pg.display.set_icon(pg.image.load("resources/graphics/icon.png"))
        # Initialize pygame
        pygame.init()
        # Display surface
        self.screen = pg.display.set_mode(
            size=self.screen_size,
            flags=pg.RESIZABLE,
        )
        # Clock
        self.clock = pg.time.Clock()
        # Caption
        self.caption = GameStrings.CAPTION
        pg.display.set_caption(self.caption)
        
        # Surface content
        # Frame
        self.frame = FrameResizable(
            rect=pg.Rect(
                0,
                0,
                self.screen_width,
                self.screen_height
            ),
            thickness=S.FRAME_THICKNESS,
            top_color=C.FRAME_TOP,
            bottom_color=C.FRAME_BOTTOM,
        )
        # Frame-camera gap
        self.frame_camera_gap = FrameResizable(
            rect=pg.Rect(
                S.FRAME_THICKNESS,
                S.FRAME_THICKNESS + S.MENUBAR_HEIGHT + S.TOOLBAR_HEIGHT,
                self.screen_width - (S.FRAME_THICKNESS * 2),
                self.screen_height - (S.FRAME_THICKNESS * 2) - S.TOOLBAR_HEIGHT - S.MENUBAR_HEIGHT
            ),
            thickness=S.FRAME_CAMERA_GAP,
            top_color=C.FRAME_CAMERA_GAP,
            bottom_color=C.FRAME_CAMERA_GAP,
            pressed=True,
        )
        # Menu
        self.menu = Menu(
            menu_bar_rect=pg.Rect(
                S.FRAME_THICKNESS,
                S.FRAME_THICKNESS,
                self.screen_width - (S.FRAME_THICKNESS * 2),
                S.MENUBAR_HEIGHT
            )
        )
        # Toolbar
        self.toolbar = Toolbar(
            rect=pg.Rect(
                S.FRAME_THICKNESS,
                self.menu.menubar.rect.bottom,
                self.menu.menubar.rect.width,
                S.TOOLBAR_HEIGHT
            )
        )
        # Camera
        self.camera = Camera(
            rect=pg.Rect(
                S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP,
                S.FRAME_THICKNESS + S.MENUBAR_HEIGHT + S.TOOLBAR_HEIGHT + S.TOOLBAR_CAMERA_GAP,
                self.screen_width - ((S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP) * 2),
                self.screen_height - (S.FRAME_THICKNESS * 2) -
                S.MENUBAR_HEIGHT - S.TOOLBAR_HEIGHT - (S.TOOLBAR_CAMERA_GAP * 2)
            ),
        )
        
        # Local event management
        self.quit_event_manager = EventManager(
            event_types=(pg.QUIT, pg.KEYDOWN),
            event_functions=(self.on_quit, self.on_keydown)
        )
        self.window_resize_event_manager = EventManager(
            event_types=[pg.VIDEORESIZE],
            event_functions=[self.on_videoresize]
        )
        self.event_managers = {
            GameSates.UNOPENED_BASIC: (
                self.window_resize_event_manager,
                self.quit_event_manager
            ),
            GameSates.OPENED_BASIC: (
                self.toolbar.event_manager,
                self.window_resize_event_manager,
                self.quit_event_manager
            ),
            GameSates.OPENED_MENU: (
                self.window_resize_event_manager,
                self.quit_event_manager
            ),
            GameSates.WINDOW: (
                self.window_resize_event_manager,
            )
        }
        
        # Global event management
        self.game_event_managers = {
            GameSates.UNOPENED_BASIC: (
                self.menu.event_manager,
                self.event_manager,
            ),
            GameSates.OPENED_BASIC: (
                self.menu.event_manager,
                self.event_manager,
            ),
            GameSates.OPENED_MENU: (
                self.menu.event_manager,
                self.event_manager,
            ),
            GameSates.WINDOW: (
                self.event_manager,
            ),
        }
        
        # Dynamic variables
        # Run
        self.frame_length = v.FRAME_LENGTH
        self.running = True
        # Event management
        self.break_event_loop = False
        self.state = GameSates.UNOPENED_BASIC
        self.isopened = GameSates.UNOPENED_BASIC
        # Draw management
        self.redraw = True
        self.draw_count = 0  # Testing
        self.draw_rects = []
        
    def run(self) -> None:
        """
        Run the game until the program is shut down
        """
        # Main game loop
        while self.running:
            # Event loop
            self.event_loop()
            # Redraw the full screen
            if self.redraw:
                self.draw()
            # Update screen
            if len(self.draw_rects) > 0:
                self.draw_count += 1
                pg.display.update(self.draw_rects)
            self.draw_rects.clear()
            # Wait for next frame
            self.clock.tick(self.frame_length)
        
        # Shutting down program
        print(f"Number of draws: {self.draw_count}")  # Testing
        pg.quit()
        sys.exit()
        
    def event_loop(self):
        """
        Main event loop of game
        """
        for event in pg.event.get():
            #print(event)
            for manager_idx in range(len(self.game_event_managers[self.state])):
                if self.game_event_managers[self.state][manager_idx](
                        event=event,
                        game=self
                ):
                    if self.break_event_loop:
                        self.break_event_loop = False
                        return
                    break
        
    def event_manager(self,
                      event: pg.event.Event,
                      *args, **kwargs,
                      ) -> bool:
        """
        Event manager for basic game events (quit, window resize)
        :param event: pygame event
        :return: True: go to next event; False: go to next event manager
        """
        for manager_idx in range(len(self.event_managers[self.state])):
            if self.event_managers[self.state][manager_idx].handle(event):
                return True
        return False
        
    def on_quit(self, *args, **kwargs) -> bool:
        """
        Quit program
        :return True: go to next event
        """
        self.running = False
        self.break_event_loop = True
        return True
    
    def on_keydown(self, event, *args, **kwargs) -> bool:
        """
        Quit program
        :param event: pygame event
        :return: True: go to next event
        """
        if event.key != pg.K_ESCAPE:
            return False
        return self.on_quit()
    
    def on_videoresize(self, event, *args, **kwargs) -> bool:
        """
        Change window size and break event loop
        :param event: pygame event
        :return: True: go to next event
        """
        # Set new screen size
        old_screen_size = self.screen_size
        self.screen_width = max(event.w, self.min_screen_size[0])
        self.screen_height = max(event.h, self.min_screen_size[1])
        self.screen_size = (self.screen_width, self.screen_height)
        # Size smaller than minimum
        if self.screen_size != event.size:
            self.screen = pg.display.set_mode(self.screen_size, flags=pg.RESIZABLE)
        # Change resizeable objects
        self.redraw = True
        if old_screen_size != self.screen_size:
            self.change_content_size()
        self.break_event_loop = True
        return True
    
    def change_content_size(self):
        """
        Resize all resizable content
        """
        # Frame
        self.frame.change_size(self.screen_size)
        # Frame camera gap
        self.frame_camera_gap.change_size(
            (self.screen_width - (S.FRAME_THICKNESS * 2),
             self.screen_height - (S.FRAME_THICKNESS * 2) - S.MENUBAR_HEIGHT - S.TOOLBAR_HEIGHT)
        )
        # Camera
        self.camera.change_size(
            (self.screen_width - ((S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP) * 2),
             self.screen_height - ((S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP) * 2) - S.MENUBAR_HEIGHT - S.TOOLBAR_HEIGHT)
        )
        # Menu
        self.menu.change_size(
            (self.screen_width - (S.FRAME_THICKNESS * 2),
             S.MENUBAR_HEIGHT)
        )
        # Toolbar
        self.toolbar.change_size(
            (self.menu.menubar.rect.width,
             S.TOOLBAR_HEIGHT))
        
    def draw(self):
        self.redraw = False
        # Clear screen
        self.screen.fill("black")
        # Content
        # Frame and gap
        self.frame.draw(self.screen)
        self.frame_camera_gap.draw(self.screen)
        # Toolbar
        self.toolbar.draw(self.screen)
        # Camera
        self.camera.draw(self.screen)
        # Menu
        self.menu.draw(self.screen)
        # Update rect
        self.draw_rects.clear()
        self.draw_rects.append(self.screen.get_rect())
