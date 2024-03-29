import pygame
import pygame as pg
import sys

from code.camera.camera import Camera

from code.game.game import Game

from code.map.map import Map

from code.menu.menu import Menu

from code.program.color_data import Colors as C
from code.program.size_data import Sizes as S
from code.program.states import FileStates, ProgramSates
from code.program.string_data import Strings as ProgramStrings
from code.program.types import FileTypes
import code.program.variable_data as v

from code.simulation.simulation import Simulation

from code.toolbar.toolbar import Toolbar

from code.util.event_manager import EventManager
from code.util.frame import FrameResizable


class Program:
    """
    Main object of program
    Contains every object of program
    After initialization the 'run' function runs until the program is shut down
    """
    def __init__(self) -> None:
        """
        Create Program object and run program
        """
        print(pg.USEREVENT)
        print(pg.NUMEVENTS - 1)
        # Data
        self.screen_width = S.SCREEN_WIDTH
        self.screen_height = S.SCREEN_HEIGHT
        self.screen_size = (self.screen_width, self.screen_height)
        self.min_screen_size = self.screen_size

        # Pygame settings
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
        pg.key.set_repeat(v.FRAME_LENGTH * 4, v.FRAME_LENGTH)
        # Caption
        self.caption = ProgramStrings.CAPTION
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
        
        # Files
        self.map = Map()
        self.simulation = Simulation()
        self.game = Game()
        self.files = {
            FileTypes.MAP: self.map,
            FileTypes.SIM: self.simulation,
            FileTypes.GAME: self.game
        }
        
        # Local event management
        self.quit_event_manager = EventManager(
            event_types=(pg.QUIT, pg.KEYDOWN),
            event_functions=(self.quit, self.keydown)
        )
        self.window_event_manager = EventManager(
            event_types=(pg.VIDEORESIZE, pg.WINDOWMOVED),
            event_functions=(self.video_resize, self.window_moved)
        )
        self.event_managers = {
            ProgramSates.UNOPENED_BASIC: (
                self.window_event_manager,
                self.quit_event_manager
            ),
            ProgramSates.OPENED_BASIC: (
                self.window_event_manager,
                self.quit_event_manager
            ),
            ProgramSates.OPENED_MENU: (
                self.window_event_manager,
                self.quit_event_manager
            ),
            ProgramSates.WINDOW: (
                self.window_event_manager,
            )
        }
        
        # Global event management
        self.program_event_managers = {
            ProgramSates.UNOPENED_BASIC: (
                self.menu.event_manager,
                self.event_manager,
            ),
            ProgramSates.OPENED_BASIC: (
                #self.toolbar.event_manager,
                self.menu.event_manager,
                self.event_manager,
            ),
            ProgramSates.OPENED_MENU: (
                self.menu.event_manager,
                self.event_manager,
            ),
            ProgramSates.WINDOW: (
                self.menu.process.event_manager,
                self.event_manager,
            ),
        }
        
        # Dynamic variables
        # Run
        self.frame_length = v.FRAME_LENGTH
        self.running = True
        # Files
        self.file_type = FileTypes.NO
        self.file_state = FileStates.EMPTY
        # Event management
        self.break_event_loop = False
        self.state = ProgramSates.UNOPENED_BASIC
        self.isopened = ProgramSates.UNOPENED_BASIC
        # Draw management
        self.redraw = True
        self.draw_count = 0  # Testing
        self.draw_rects = []
        
        # Data setting
        self.menu.set_inactive_list_elements(self)
        
    def run(self) -> None:
        """
        Run the program until the program is shut down
        """
        # Main program loop
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
        Main event loop of program
        """
        for event in pg.event.get():
            #print(event)
            for manager_idx in range(len(self.program_event_managers[self.state])):
                if self.program_event_managers[self.state][manager_idx](
                        event=event,
                        program=self
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
        Event manager for basic program events (quit, window resize)
        :param event: pygame event
        :return: True: go to next event; False: go to next event manager
        """
        for manager_idx in range(len(self.event_managers[self.state])):
            if self.event_managers[self.state][manager_idx].handle(event):
                return True
        return False
        
    def quit(self,
             *args, **kwargs) -> bool:
        """
        Quit program
        :return True: go to next event
        """
        self.running = False
        self.break_event_loop = True
        return True
    
    def keydown(self,
                event: pg.event.Event,
                *args, **kwargs) -> bool:
        """
        Quit program
        :param event: pygame event
        :return: True: go to next event; False: go to next event handler
        """
        if event.key != pg.K_ESCAPE:
            return False
        return self.quit()
    
    def video_resize(self,
                     event: pg.event.Event,
                     *args, **kwargs) -> bool:
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
    
    def window_moved(self,
                     *args, **kwargs) -> bool:
        """
        Redraw window when moved
        :return: True: go to next event
        """
        self.redraw = True
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
        if self.state == ProgramSates.WINDOW:
            for window in self.menu.process.window.values():
                window.reposition(self.screen.get_rect().center)
        # Toolbar
        self.toolbar.change_size(
            new_size=(
                self.menu.menubar.rect.width,
                S.TOOLBAR_HEIGHT,
            ),
        )
        
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
        
    def get_file_code(self) -> int:
        """
        Get file code
        :return: file_type * 10 + file_state
        """
        return self.file_type * 10 + self.file_state
