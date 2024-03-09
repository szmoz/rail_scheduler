import pygame as pg

from code.util.background import BackgroundResizable
from code.util.event_manager import EventManager

from code.toolbar.color_data import ToolbarColors as C
from code.toolbar.size_data import ToolbarSizes as S
from code.toolbar.states import ToolbarStates
from code.toolbar.string_data import ToolbarStrings as Strings


class Toolbar:
    """
    Toolbar object
    Can be map creator, scheduler, simulator toolbar
    """
    def __init__(self,
                 rect: pg.Rect,
                 ) -> None:
        """
        Initialize Toolbar
        :param rect: rectangle area of toolbar
        """
        # Surface content
        # Background
        self.background = BackgroundResizable(
            rect=rect,
            color=C.BACKGROUND
        )
        
        # Event management
        self.event_managers = {
            ToolbarStates.MAP: EventManager(
                event_types=(None,),
                event_functions=(None,)
            ),
            ToolbarStates.SCHEDULE: EventManager(
                event_types=(None,),
                event_functions=(None,)
            ),
            ToolbarStates.SIMULATION: EventManager(
                event_types=(None,),
                event_functions=(None,)
            )
        }
        
        # Dynamic variables
        self.state = ToolbarStates.CLOSED
        
    def event_manager(self,
                      event: pg.event.Event,
                      game,
                      ) -> bool:
        """
        Event manager for menu
        :param event: pygame event
        :param game: Game object
        :return: True: go to next event; False: go to next event manager
        """
        return self.event_managers[self.state].handle(
            event=event,
            game=game
        )
    
    def draw(self,
             surf: pg.Surface
             ) -> pg.Rect:
        """
        Draw all toolbar content on surface
        :param surf: surface
        :return rect area to draw
        """
        # Background
        self.background.draw(surf)
        if self.state == ToolbarStates.CLOSED:
            return self.background.rect
        
    def change_size(self,
                    new_size: tuple or list,
                    ) -> None:
        """
        Change size of toolbar
        All element stay at same position
        :param new_size: new size of toolbar background
        """
        self.background.change_size(new_size)
        