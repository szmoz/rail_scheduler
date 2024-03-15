import pygame as pg

from code.menu.color_data import Colors as C
from code.menu.menubar import MenuBar
from code.menu.menulist import Menulist
from code.menu.menu_process import MenuProcess
from code.menu.size_data import Sizes as S
from code.menu.states import MenuStates
from code.menu.string_data import Strings as StringData
from code.menu.variable_data import ButtonFrameEdgeLines

from code.util.event_manager import EventManager


class Menu:
    """
    Menu object
    Contains a menubar and dropdown lists
    """
    def __init__(self,
                 menu_bar_rect: pg.Rect,
                 ) -> None:
        """
        Initialize Menu object
        :param menu_bar_rect: rectangle area of menubar
        """
        # Modules
        self.menubar = MenuBar(
            rect=menu_bar_rect,
            background_color=C.MENU_BACKGROUND,
            button_width=S.BUTTON_WIDTH,
            button_background_color=C.BUTTON_BACKGROUND,
            button_background_color_pressed=C.BUTTON_BACKGROUND_PRESSED,
            button_background_color_over=C.BUTTON_BACKGROUND_OVER,
            button_frame_thickness=S.BUTTON_FRAME_THICKNESS,
            button_frame_top_color=C.BUTTON_FRAME_TOP,
            button_frame_bottom_color=C.BUTTON_FRAME_BOTTOM,
            button_frame_edge_lines=ButtonFrameEdgeLines.STANDARD,
            button_frame_top_color_pressed=C.BUTTON_FRAME_TOP_PRESSED,
            button_frame_bottom_color_pressed=C.BUTTON_FRAME_BOTTOM_PRESSED,
            button_frame_edge_lines_pressed=ButtonFrameEdgeLines.PRESSED,
            button_frame_edge_lines_over=ButtonFrameEdgeLines.OVER,
            button_texts=StringData.BUTTON,
            text_type=StringData.BUTTON_TYPE,
            text_size=S.BUTTON_TEXT,
            text_color=C.BUTTON_TEXT
        )
        self.menulists = dict()
        for i in range(len(StringData.BUTTON)):
            self.menulists[i] = Menulist(
                topleft=self.menubar.buttons[i].rect.bottomleft,
                background_color=C.LIST_BACKGROUND,
                background_color_over=C.LIST_BACKGROUND_OVER,
                frame_thickness=S.LIST_FRAME_THICKNESS,
                frame_top_color=C.LIST_FRAME_TOP,
                frame_bottom_color=C.LIST_FRAME_BOTTOM,
                texts=StringData.LISTS[i],
                text_type=StringData.LIST_TYPE,
                text_size=S.LIST_TEXT,
                text_color=C.LIST_TEXT
            )

        # Menu processor
        self.process = MenuProcess()
        
        # Event management
        self.close_event_manager = EventManager(
            event_types=(pg.MOUSEBUTTONDOWN, pg.KEYDOWN, pg.QUIT),
            event_functions=(self.click_outside, self.menubar.close_menu_with_esc, self.close_menu_quit)
        )
        
        self.event_managers = {
            MenuStates.CLOSED: (
                self.menubar.event_manager,
            ),
            MenuStates.OPENED: (
                self.menulist_event_manager,
                self.menubar.event_manager,
                self.check_close_event_manager,
            ),
            MenuStates.PROCESS: (
                self.process.event_manager,
            )
        }
        
        # Dynamic variables
        self.state = MenuStates.CLOSED
        self.list_opened = -1
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for menu
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        for manager_idx in range(len(self.event_managers[self.state])):
            if program.break_event_loop:
                return True
            if self.event_managers[self.state][manager_idx](
                    event=event,
                    program=program,):
                return True
        return False
        
    def menulist_event_manager(self,
                               event: pg.event.Event,
                               program,
                               ) -> bool:
        """
        Event manager for menulist
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        return self.menulists[self.list_opened].event_manager.handle(
            event=event,
            program=program)
    
    def check_close_event_manager(self,
                                  event: pg.event.Event,
                                  program,
                                  ) -> bool:
        """
        Event manager for menu closing
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        return self.close_event_manager.handle(
            event=event,
            program=program)
    
    def click_outside(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Close menu
        Click is outside of menubar buttons and active menulist elements (can be menulist frame)
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Collision with Menulist frame
        if self.menulists[self.list_opened].rect.collidepoint(event.pos):
            return True
        # Close menu
        return self.menubar.close_menu_with_esc(
            event=pg.event.Event(
                pg.KEYDOWN,
                key=pg.K_ESCAPE
            ),
            program=program)
        
    def close_menu_quit(self,
                        program=None,
                        *args, **kwargs) -> bool:
        """
        Close menu when quit
        :param program: Program object
        :return: False: go to next manager (event has to get to program's quit_event_manager)
        """
        self.menubar.close_menu_with_esc(
            event=pg.event.Event(
                pg.KEYDOWN,
                key=pg.K_ESCAPE
            ),
            program=program)
        return False
    
    def draw(self,
             surf: pg.Surface
             ) -> pg.Rect:
        """
        Draw all menu content on surface
        :param surf: surface
        :return rect area to draw
        """
        # Menubar
        self.menubar.draw(surf)
        # Menulist
        if self.list_opened >= 0:
            self.menulists[self.list_opened].draw(surf)
            return pg.Rect(
                self.menubar.rect.left,
                self.menubar.rect.top,
                self.menubar.rect.width,
                self.menubar.rect.height + self.menulists[self.list_opened].rect.height
            )
        if len(self.process.window) > 0:
            for window in self.process.window.values():
                window.draw(surf)
            return surf.get_rect()
        return self.menubar.rect
    
    def change_size(self,
                    new_size: tuple or list,
                    ) -> None:
        """
        Change size of menubar
        All buttons and lists stay at same position
        :param new_size: new size of menubar background
        """
        self.menubar.change_size(new_size)
