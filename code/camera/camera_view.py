import pygame as pg

import code.camera.event_handlers_map as event_handler_map
from code.camera.states import CameraStates as States
from code.camera.states import MapStates

from code.util.event_manager import EventManager


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
        self.rect = rect
        
        # Event management
        self.event_managers = {
            States.MAP: {
                MapStates.STANDARD: EventManager(
                    event_types=(
                        pg.MOUSEBUTTONDOWN,
                        pg.MOUSEBUTTONUP,
                        pg.MOUSEMOTION,
                    ),
                    event_functions=(
                        event_handler_map.standard_mousebuttondown,
                        event_handler_map.standard_mousebuttonup,
                        event_handler_map.standard_mousemotion,
                    ),
                ),
            },
            
        }
        
        # Dynamic variables
        self.file_type = States.EMPTY
        self.state = MapStates.STANDARD
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for camera
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        try:
            return self.event_managers[self.file_type][self.state].handle(
                    event=event,
                    program=program,
            )
        except KeyError:
            return False
    
    def change_file_type(self,
                         new_file_type: int,
                         ) -> None:
        """
        Change file type
        :param new_file_type: file type code
        """
        self.file_type = new_file_type
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw view image on surface
        :param surf: surface drawn onto
        :return rect area to draw
        """
        return self.rect

    def change_size(self,
                    new_size: tuple):
        """
        Update camera view basic size and reset map rectangle area
        :param new_size: new size of background (width, height)
        """
        # Update rect
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
