import pygame as pg


class CameraView:
    """
    Camera view over map
    """
    def __init__(self,
                 rect: pg.Rect):
        """
        Initialize camera view
        :param rect: rectangle area where view image is drawn
        """
        # Data
        self.rect = rect
        
        # Map dynamic variables
        self.map_rect = pg.Rect(0, 0, 0, 0)
        
    def draw(self,
             surf: pg.Surface,
             map_surf: pg.Surface = None,
             ) -> pg.Rect:
        """
        Draw view image on surface
        :param surf: surface
        :param map_surf: Map object's surface
        :return rect area to draw
        """
        surf.blit(map_surf, self.rect, area=self.map_rect)
        return self.rect
        