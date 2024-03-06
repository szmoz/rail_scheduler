import pygame as pg

from code.camera.camera_view import CameraView
from code.camera.colors import Colors as C
from code.camera.sizes import Sizes as S

from code.util.background import BackgroundResizable
from code.util.frame import FrameResizable


class Camera(pg.sprite.Sprite):
    """
    Workspace area with frame
    Functions as a camera over the map
    """
    def __init__(self,
                 rect: pg.Rect) -> None:
        """
        Initialize Camera object
        :param rect: rectangle area on surface
        """
        super().__init__()
        self.image = pg.Surface(rect.size)
        self.rect = rect
        
        # Main surface content
        # Frame
        self.frame = FrameResizable(
            rect=self.rect,
            thickness=S.FRAME_THICKNESS,
            top_color=C.FRAME_TOP,
            bottom_color=C.FRAME_BOTTOM,
        )
        # Camera views
        # Empty camera view -- when camera does not show anything
        self.empty_camera_view = BackgroundResizable(
            rect=pg.Rect(
                self.rect.left + S.FRAME_THICKNESS,
                self.rect.top + S.FRAME_THICKNESS,
                self.rect.width - (S.FRAME_THICKNESS * 2),
                self.rect.height - (S.FRAME_THICKNESS * 2)
            ),
            color=C.BACKGROUND,
        )
        # Camera view
        self.map_camera_view = CameraView(rect=self.empty_camera_view.rect)
        self.camera_views = (self.empty_camera_view, self.map_camera_view)
        self.map_surfs = (None, None)  # NEED TO CHANGE [1]--------------------------
        
        # Dynamic variables
        self.active_camera_view_idx = 0
        
    def on_redraw(self,
                  surf: pg.Surface):
        """
        Redraw all surface content
        :param surf: surface
        """
        # Frame
        self.frame.draw(surf)
        # Camera screen
        self.
        
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
        # Surface
        self.image = pg.Surface(self.rect.size)
        # Frame
        self.frame.change_size(new_size)
        print(self.frame.sprites())
        # Empty camera view
        self.empty_camera_view.change_size(
            (new_size[0] - (S.FRAME_THICKNESS * 2),
             new_size[1] - (S.FRAME_THICKNESS * 2))
        )
        