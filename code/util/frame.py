import pygame as pg


class Frame(pg.sprite.Group):
    """
    Frame object
    Contains Sprites
    """
    def __init__(self,
                 rect: pg.Rect,
                 thickness: int,
                 top_color: tuple or list,
                 bottom_color: tuple or list,
                 pressed: bool = False,
                 edge_lines: tuple or list = None,
                 ) -> None:
        """
        Initialize Frame object
        :param rect: rectangle that needs to be framed (inclusively)
        :param thickness: frame thickness
        :param top_color: frame left & top color
        :param bottom_color: frame bottom & right color
        :param pressed: True: bottomleft & topright corners are squared and topcolored
        :param edge_lines: +:outer; -:inner; 1:left; 2:top; 3:right; 4:bottom
        """
        # Initialize sprite.Group object
        super().__init__()
        
        # Data
        self.rect = rect
        self.thickness = thickness
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.pressed = pressed
        self.edge_lines = edge_lines
        
        # Sprites
        self.update_sprites()
        
    def change_size(self,
                    new_size: tuple or int,
                    ) -> None:
        """
        Update frame size and recreate sprites
        :param new_size: new size of rectangle that needs to be framed (inclusively)
        """
        # Update data
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
        # Update sprites
        self.update_sprites()
        
    def update_sprites(self) -> None:
        """
        Update sprites
        """
        self.empty()
        # Left
        left = pg.sprite.Sprite(self)
        left.image = pg.Surface((self.thickness, self.rect.height))
        left.image.fill(self.top_color)
        left.rect = left.image.get_rect()
        left.rect.topleft = self.rect.topleft
        # Top
        top = pg.sprite.Sprite(self)
        top.image = pg.Surface((self.rect.width, self.thickness))
        top.image.fill(self.top_color)
        top.rect = top.image.get_rect()
        top.rect.topleft = self.rect.topleft
        # Right
        right = pg.sprite.Sprite(self)
        right.image = pg.Surface((self.thickness, self.rect.height - self.thickness))
        right.image.fill(self.bottom_color)
        right.rect = right.image.get_rect()
        right.rect.bottomright = self.rect.bottomright
        # Bottom
        bottom = pg.sprite.Sprite(self)
        bottom.image = pg.Surface((self.rect.width - self.thickness, self.thickness))
        bottom.image.fill(self.bottom_color)
        bottom.rect = bottom.image.get_rect()
        bottom.rect.bottomright = self.rect.bottomright
        # Edge lines
        if self.edge_lines is None:
            edge_lines = []
    
        # Corners
        if self.pressed:
            return
        # Bottomleft corner
        pg.draw.polygon(
            surface=left.image,
            color=self.bottom_color,
            points=(
                left.rect.bottomleft,
                left.rect.bottomright,
                (left.rect.right, left.rect.bottom - self.thickness)
            )
        )
        # Topright corner
        pg.draw.polygon(
            surface=top.image,
            color=self.bottom_color,
            points=(
                top.rect.topright,
                top.rect.bottomright,
                (top.rect.right - self.thickness, top.rect.bottom)
            )
        )
        