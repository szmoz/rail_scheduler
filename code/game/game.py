import pygame
import pygame as pg
import sys

from code.game.sizes import Sizes as S
import code.game.variables as v


class Game:
    """
    Main object of program
    Contains every object of program
    After initialization the 'run' function runs until the program is shut down
    """
    def __init__(self):
        """
        Create Game object and run game
        """
        # Initialize pygame
        pygame.init()
        self.screen = pg.display.set_mode(
            size=(S.SCREEN_WIDTH, S.SCREEN_HEIGHT),
            flags=pg.RESIZABLE,
        )
        self.clock = pg.time.Clock()
        
        # Dynamic variables
        self.running = True
        self.redraw = True
        self.draw_count = 0  # Testing
        self.run()
        
    def run(self):
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
                pg.display.flip()
            # Wait for next frame
            self.clock.tick(v.FRAMERATE)

        print(f"Number of draws: {self.draw_count}")  # Testing
        pg.quit()
        sys.exit()
        
        