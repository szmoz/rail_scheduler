import pygame as pg


class Text(pg.sprite.Sprite):
    """
    Text sprite
    """
    def __init__(self,
                 text: str,
                 text_type: str,
                 size: int,
                 color: tuple or list,
                 anchor_type: str,
                 anchor_pos: tuple or list):
        """
        Initialize Text object
        :param text: text
        :param text_type: path to '.ttf' file
        :param size: size of text
        :param color: color of text
        :param anchor_type: anchoring type. Can be: center, midleft, midright, bottomleft, bottomright
        :param anchor_pos: anchoring position
        """
        super().__init__()
        # Data
        self.color = color
        self.type = text_type
        self.size = size
        self.text = text
        # Surface content
        self.font = pg.font.Font(self.type, self.size)
        self.image = self.font.render(self.text, True, self.color)
        # Rect
        self.rect = self.image.get_rect()
        # Anchoring
        self.anchor_pos = anchor_pos
        anchor_functions = {
            'center': self.anchor_center,
            'midleft': self.anchor_midleft,
            'midright': self.anchor_midright,
            'bottomleft': self.anchor_bottomleft,
            'bottomright': self.anchor_bottomright
        }
        self.anchoring = anchor_functions[anchor_type]
        self.anchoring()
    
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw Text object on surface
        :param surf: surface
        :return rect area to update on screen
        """
        surf.blit(self.image, self.rect)
        return self.rect
    
    def change_text(self,
                    new_text: str,
                    ) -> None:
        """
        Change text and position according to anchoring point
        """
        self.text = new_text
        self.image = self.font.render(self.text, True, self.color)
        # Rect
        self.rect = self.image.get_rect()
        self.anchoring()
        
    def change_color(self,
                     new_color: tuple or list
                     ) -> None:
        """
        Change color of text
        """
        self.color = new_color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.anchoring()
        
    def change_anchor_pos(self,
                          new_anchor_pos: tuple,
                          ) -> None:
        """
        Change anchoring position of Text object
        :param new_anchor_pos: new anchoring position
        """
        self.anchor_pos = new_anchor_pos
        self.anchoring()

    def anchor_center(self):
        self.rect.center = self.anchor_pos

    def anchor_midleft(self):
        self.rect.midleft = self.anchor_pos

    def anchor_midright(self):
        self.rect.midright = self.anchor_pos

    def anchor_bottomleft(self):
        self.rect.bottomleft = self.anchor_pos

    def anchor_bottomright(self):
        self.rect.bottomright = self.anchor_pos

    def reposition(self,
                   x_diff: int = 0,
                   y_diff: int = 0,
                   ) -> None:
        """
        Reposition textbox
        :param x_diff: x difference to add
        :param y_diff: y difference to add
        """
        self.rect.x += x_diff
        self.rect.y += y_diff
        self.anchor_pos = (
            self.anchor_pos[0] + x_diff,
            self.anchor_pos[1] + y_diff
        )
        
    def __repr__(self):
        return self.text
        