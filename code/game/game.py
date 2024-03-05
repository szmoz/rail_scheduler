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
        # Initialize pygame
        pygame.init()
        self.screen = pg.display.set_mode(
            size=self.screen_size,
            flags=pg.RESIZABLE,
        )
        self.clock = pg.time.Clock()
        
        # Static surface content
        self.static_surf_content = pg.sprite.Group()
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
        self.static_surf_content.add(self.frame)
        
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
            # Update screen
            if self.redraw:
                self.redraw = False
                self.draw_count += 1  # Testing
                self.static_surf_content.draw(self.screen)
                pg.display.flip()
            # Wait for next frame
            self.clock.tick(self.frame_length)

        print(f"Number of draws: {self.draw_count}")  # Testing
        pg.quit()
        sys.exit()
        
        