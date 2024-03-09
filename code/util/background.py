import pygame as pg


class Background(pg.sprite.Sprite):
    """
    Basic Background sprite with one color
    """
    def __init__(self,
                 rect: pg.Rect,
                 color: tuple):
        """
        Initialize Background object
        :param rect: rectangle area on surface
        :param color: background color
        """
        super().__init__()
        
        self.image = pg.Surface(rect.size)
        self.image.fill(color)
        self.rect = rect
        
    def draw(self,
             surf: pg.Surface,
             *args, **kwargs) -> pg.Rect:
        """
        Draw background on surface
        :param surf: Surface
        :return rect area to draw
        """
        surf.blit(self.image, self.rect)
        return self.rect
        
        
class BackgroundResizable(Background):
    """
    Basic resizable background sprite with one color
    """
    def __init__(self,
                 rect: pg.Rect,
                 color: tuple):
        """
        Initialize Resizable Background object
        :param rect: rectangle area on surface
        :param color: background color
        """
        super().__init__(
            rect=rect,
            color=color
        )
        # Data
        self.color = color
        
    def change_size(self,
                    new_size: tuple or int):
        """
        Update background size and redraw surface
        :param new_size: new size of background
        """
        # Update rect
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
        # Update surface
        self.image = pg.Surface(new_size)
        self.image.fill(self.color)
        