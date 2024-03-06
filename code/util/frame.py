import pygame as pg


from code.util.colors import Colors as C


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
        
        # Sprites
        self.update_sprites(
            top_color=top_color,
            bottom_color=bottom_color,
            pressed=pressed,
            edge_lines=edge_lines
        )
        
    def update_sprites(self,
                       top_color=None,
                       bottom_color=None,
                       pressed=None,
                       edge_lines=None) -> None:
        """
        Update sprites
        """
        self.empty()
        # Left
        left = pg.sprite.Sprite(self)
        left.image = pg.Surface((self.thickness, self.rect.height))
        left.image.fill(top_color)
        left.rect = left.image.get_rect()
        left.rect.topleft = self.rect.topleft
        # Top
        top = pg.sprite.Sprite(self)
        top.image = pg.Surface((self.rect.width, self.thickness))
        top.image.fill(top_color)
        top.rect = top.image.get_rect()
        top.rect.topleft = self.rect.topleft
        # Right
        right = pg.sprite.Sprite(self)
        right.image = pg.Surface((self.thickness, self.rect.height - self.thickness))
        right.image.fill(bottom_color)
        right.rect = right.image.get_rect()
        right.rect.bottomright = self.rect.bottomright
        # Bottom
        bottom = pg.sprite.Sprite(self)
        bottom.image = pg.Surface((self.rect.width - self.thickness, self.thickness))
        bottom.image.fill(bottom_color)
        bottom.rect = bottom.image.get_rect()
        bottom.rect.bottomright = self.rect.bottomright
        
        # Corners
        if not pressed:
            # Bottomleft corner
            pg.draw.polygon(
                surface=left.image,
                color=bottom_color,
                points=(
                    left.rect.bottomleft,
                    left.rect.bottomright,
                    (left.rect.right, left.rect.bottom - self.thickness)
                )
            )
            # Topright corner
            pg.draw.polygon(
                surface=top.image,
                color=bottom_color,
                points=(
                    top.rect.topright,
                    top.rect.bottomright,
                    (top.rect.right - self.thickness, top.rect.bottom)
                )
            )

        # Edge lines
        if edge_lines is None:
            return
        edge_surf_data = (
            None,  # idx:0
            (left.rect.topleft, (1, left.rect.height)),  # idx:1
            (top.rect.topleft, (top.rect.width, 1)),  # idx:2
            ((top.rect.right - 1, top.rect.top), (1, left.rect.height)),  # idx:3
            ((left.rect.left, left.rect.bottom - 1), (top.rect.width, 1)),  # idx:4
            None,  # idx:5
            ((left.rect.right, bottom.rect.top), (top.rect.width - (self.thickness * 2), 1)),  # idx:-4
            ((right.rect.left, right.rect.top), (1, left.rect.height - (self.thickness * 2))),  # idx:-3
            ((left.rect.right, top.rect.bottom - 1), (top.rect.width - (self.thickness * 2), 1)),  # idx:-2
            ((left.rect.right - 1, top.rect.bottom), (1, left.rect.height - (self.thickness * 2))),  # idx:-1
        )
        for line_idx in edge_lines:
            if line_idx % 2 == 0:  # top & bottom: horizontal lines
                end_x = edge_surf_data[line_idx][1][0]
                line = pg.sprite.Sprite(self)
                line.image = pg.Surface(edge_surf_data[line_idx][1])
                line.image.set_colorkey(C.BLACK)
                for act_x in range(0, end_x + 1, 2):
                    pg.draw.line(line.image,
                                 C.DARK_GRAY,
                                 (act_x, 0),
                                 (act_x, 0))
                line.rect = line.image.get_rect()
                line.rect.topleft = edge_surf_data[line_idx][0]
                continue
            # right & left: vertical lines
            end_y = edge_surf_data[line_idx][1][1]
            line = pg.sprite.Sprite(self)
            line.image = pg.Surface(edge_surf_data[line_idx][1])
            line.image.set_colorkey(C.BLACK)
            for act_y in range(0, end_y + 1, 2):
                pg.draw.line(line.image,
                             C.DARK_GRAY,
                             (0, act_y),
                             (0, act_y))
            line.rect = line.image.get_rect()
            line.rect.topleft = edge_surf_data[line_idx][0]
        
        
class FrameResizable(Frame):
    def __init__(self,
                 rect: pg.Rect,
                 thickness: int,
                 top_color: tuple or list,
                 bottom_color: tuple or list,
                 pressed: bool = False,
                 edge_lines: tuple or list = None,
                 ) -> None:
        super().__init__(
            rect=rect,
            thickness=thickness,
            top_color=top_color,
            bottom_color=bottom_color,
            pressed=pressed,
            edge_lines=edge_lines
        )
        
        # Data
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.pressed = pressed
        self.edge_lines = edge_lines
        
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
        self.update_sprites(
            top_color=self.top_color,
            bottom_color=self.bottom_color,
            pressed=self.pressed,
            edge_lines=self.edge_lines
        )
        