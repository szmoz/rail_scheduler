import pygame as pg

from code.camera.camera_view import CameraView
from code.camera.color_data import Colors as C
from code.camera.size_data import Sizes as S

from code.util.frame import FrameResizable


class Camera:
    """
    Workspace area with frame
    Functions as a camera over the map
    """
    def __init__(self,
                 rect: pg.Rect,
                 map_obj,
                 ) -> None:
        """
        Initialize Camera object
        :param rect: rectangle area on surface
        :param map_obj: program.map
        """
        self.rect = rect
        
        # Main surface content
        # Frame
        self.frame = FrameResizable(
            rect=self.rect,
            thickness=S.FRAME_THICKNESS,
            top_color=C.FRAME_TOP,
            bottom_color=C.FRAME_BOTTOM,
        )
        # Camera view
        self.view = CameraView(
            rect=pg.Rect(
                self.rect.left + S.FRAME_THICKNESS,
                self.rect.top + S.FRAME_THICKNESS,
                self.rect.width - (S.FRAME_THICKNESS * 2),
                self.rect.height - (S.FRAME_THICKNESS * 2)
            ),
            map_obj=map_obj,
        )
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Redraw all surface content
        :param surf: surface
        :return rect area to draw
        """
        # Frame
        self.frame.draw(surf)
        # View
        self.view.draw(surf)
        return self.rect
        
    def change_size(self,
                    new_size: tuple or list):
        """
        Resize all resizable content
        :param new_size: new size of rectangle
        """
        # Rect
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
        # Frame
        self.frame.change_size(new_size)
        # View
        self.view.change_size(
            new_size=(
                new_size[0] - (self.frame.thickness * 2),
                new_size[1] - (self.frame.thickness * 2),
            ),
        )
        