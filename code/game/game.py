import pygame
import pygame as pg
import sys

from code.camera.camera import Camera

from code.game.colors import Colors as C
from code.game.sizes import Sizes as S
import code.game.variables as v

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
        # Data
        self.screen_width = S.SCREEN_WIDTH
        self.screen_height = S.SCREEN_HEIGHT
        self.screen_size = (self.screen_width, self.screen_height)
        self.min_screen_size = self.screen_size
        # Initialize pygame
        pygame.init()
        self.screen = pg.display.set_mode(
            size=self.screen_size,
            flags=pg.RESIZABLE,
        )
        self.clock = pg.time.Clock()
        
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
        # Menubar
        # Toolbar
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
        
        # Event managers
        self.event_manager = EventManager(
            event_types=(pg.QUIT, pg.KEYDOWN, pg.VIDEORESIZE),
            event_functions=(self.on_quit, self.on_keydown, self.on_videoresize)
        )
        
        # Dynamic variables
        self.frame_length = v.FRAME_LENGTH
        self.running = True
        self.redraw = True
        self.draw_count = 0  # Testing
        self.run()
        
    def run(self) -> None:
        """
        Run the game until the program is shut down
        """
        print(pg.USEREVENT)
        print(pg.NUMEVENTS - 1)
        # Main game loop
        while self.running:
            # Event loop
            for event in pg.event.get():
                if self.event_manager.handle(event):
                    continue
                
            # Redraw the full screen
            if self.redraw:
                self.redraw = False
                self.draw_count += 1  # Testing
                self.on_redraw()
                
            # Update screen
            pg.display.flip()
            # Wait for next frame
            self.clock.tick(self.frame_length)
        
        # Shutting down program
        print(f"Number of draws: {self.draw_count}")  # Testing
        pg.quit()
        sys.exit()
        
    def on_redraw(self):
        # Clear screen
        self.screen.fill("black")
        # Content
        self.frame.draw(self.screen)
        self.frame_camera_gap.draw(self.screen)
        self.camera.on_redraw(self.screen)

    def on_quit(self, *args, **kwargs):
        self.running = False
        return True
    
    def on_keydown(self, event, *args, **kwargs):
        if event.key != pg.K_ESCAPE:
            return False
        return self.on_quit()
    
    def on_videoresize(self, event, *args, **kwargs):
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
        return True
    
    def change_content_size(self):
        """
        Resize all resizable content
        """
        self.frame.change_size(self.screen_size)
        self.frame_camera_gap.change_size(
            (self.screen_width - (S.FRAME_THICKNESS * 2),
             self.screen_height - (S.FRAME_THICKNESS * 2) - S.MENUBAR_HEIGHT - S.TOOLBAR_HEIGHT)
        )
        self.camera.change_size(
            (self.screen_width - ((S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP) * 2),
             self.screen_height - ((S.FRAME_THICKNESS + S.FRAME_CAMERA_GAP) * 2) - S.MENUBAR_HEIGHT - S.TOOLBAR_HEIGHT)
        )
        