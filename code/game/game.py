import pygame
import pygame as pg
import sys

from code.game.colors import Colors as C
from code.game.sizes import Sizes as S
import code.game.variables as v

from code.util.frame import Frame


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
        
        # Frame
        self.frame = Frame(
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
            # ---------TEST----------
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                    break
                elif event.type == pg.VIDEORESIZE:
                    self.screen_width = max(event.w, self.min_screen_size[0])
                    self.screen_height = max(event.h, self.min_screen_size[1])
                    self.screen_size = (self.screen_width, self.screen_height)
                    if self.screen_size != event.size:
                        self.screen = pg.display.set_mode(self.screen_size, flags=pg.RESIZABLE)
                    self.redraw = True
                    self.frame.change_size(self.screen_size)
                    break
            # Redraw the full screen
            if self.redraw:
                self.redraw = False
                self.draw_count += 1  # Testing
                # Clear screen
                self.screen.fill("black")
                # Content
                self.frame.draw(self.screen)
                # Update screen
                pg.display.flip()
            # Wait for next frame
            self.clock.tick(self.frame_length)

        print(f"Number of draws: {self.draw_count}")  # Testing
        pg.quit()
        sys.exit()
        
        