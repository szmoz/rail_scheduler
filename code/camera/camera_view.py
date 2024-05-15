import pygame as pg

from code.camera.color_data import Colors as C
from code.camera.states import MapStates

from code.program.types import FileTypes

from code.util.event_manager import EventManager


class CameraView:
    """
    Camera view over map
    """
    def __init__(self,
                 rect: pg.Rect,
                 map_obj,
                 ) -> None:
        """
        Initialize camera view
        :param rect: rectangle area where view image is drawn
        :param map_obj: program.map
        """
        self.rect = rect
        self.map = map_obj
        self.tile_size = 21
        
        # Event management
        self.event_managers = {
            FileTypes.MAP: {
                MapStates.STANDARD: EventManager(
                    event_types=(
                        pg.MOUSEBUTTONDOWN,
                        pg.KEYDOWN,
                        pg.MOUSEMOTION,
                        pg.MOUSEWHEEL,
                    ),
                    event_functions=(
                        self.start_moving_map,
                        self.standard_keydown,
                        self.standard_mousemotion,
                        self.standard_mousewheel,
                    ),
                ),
                MapStates.MOVE: EventManager(
                    event_types=(
                        pg.MOUSEMOTION,
                        pg.MOUSEBUTTONUP,
                    ),
                    event_functions=(
                        self.moving_map_with_mouse,
                        self.stop_moving_map,
                    )
                ),
            },
            
        }
        
        # Graphic content
        self.surfs = {}
        self.tile_count_surf = 10
        self.surf_size = self.tile_count_surf * self.tile_size
        self.line_thickness = 3
        self.background_color = C.STANDARD_BACKGROUND
        self.line_color = C.STANDARD_LINE
        
        # Terrain colors
        self.terrain_codes = {
            0: C.STANDARD_BACKGROUND,
            1: C.TERRAIN_FOREST,
            2: C.TERRAIN_CITY,
            3: C.TERRAIN_DESERT,
            4: C.TERRAIN_WATER,
        }
        
        # Rail images
        self.straight_img = pg.image.load("resources/graphics/rail_straight.BMP").convert()
        self.straight_img.set_colorkey(self.background_color)
        self.straight_img_rot_90 = pg.transform.rotate(self.straight_img, 90)
        self.diag_img = pg.image.load("resources/graphics/rail_diag.BMP").convert()
        self.diag_img.set_colorkey(self.background_color)
        self.diag_img_rot_90 = pg.transform.rotate(self.diag_img, 90)
        self.turn_img = pg.image.load("resources/graphics/rail_turn.BMP").convert()
        self.turn_img.set_colorkey(self.background_color)
        self.turn_img_rot_90 = pg.transform.rotate(self.turn_img, 90)
        self.turn_img_rot_180 = pg.transform.rotate(self.turn_img, 180)
        self.turn_img_rot_270 = pg.transform.rotate(self.turn_img, 270)
        self.diagturn_img = pg.image.load("resources/graphics/rail_diagturn.BMP").convert()
        self.diagturn_img.set_colorkey(self.background_color)
        self.diagturn_img_rot_90 = pg.transform.rotate(self.diagturn_img, 90)
        self.diagturn_img_rot_180 = pg.transform.rotate(self.diagturn_img, 180)
        self.diagturn_img_rot_270 = pg.transform.rotate(self.diagturn_img, 270)
        self.bend_img = pg.image.load("resources/graphics/rail_bend.BMP").convert()
        self.bend_img.set_colorkey(self.background_color)
        self.bend_img_rot_90 = pg.transform.rotate(self.bend_img, 90)
        self.bend_img_rot_180 = pg.transform.rotate(self.bend_img, 180)
        self.bend_img_rot_270 = pg.transform.rotate(self.bend_img, 270)
        self.diagbend_img = pg.image.load("resources/graphics/rail_diagbend.BMP").convert()
        self.diagbend_img.set_colorkey(self.background_color)
        self.diagbend_img_rot_90 = pg.transform.rotate(self.diagbend_img, 90)
        self.diagbend_img_rot_180 = pg.transform.rotate(self.diagbend_img, 180)
        self.diagbend_img_rot_270 = pg.transform.rotate(self.diagbend_img, 270)
        self.rail_image_codes = {
            2: self.diagturn_img,
            5: self.bend_img_rot_270,
            6: self.diagturn_img_rot_90,
            7: self.diagbend_img,
            8: self.diag_img,
            13: self.turn_img,
            15: self.turn_img_rot_270,
            16: self.bend_img,
            17: self.straight_img,
            18: self.diagbend_img_rot_180,
            23: self.diagbend_img_rot_270,
            26: self.diag_img_rot_90,
            27: self.bend_img_rot_180,
            28: self.diagturn_img_rot_270,
            35: self.straight_img_rot_90,
            37: self.turn_img_rot_90,
            38: self.bend_img_rot_90,
            56: self.diagbend_img_rot_90,
            57: self.turn_img_rot_180,
            68: self.diagturn_img_rot_180,
        }
        self.diag_corner_img = pg.image.load("resources/graphics/rail_diag_corner.BMP").convert()
        self.diag_corner_img.set_colorkey(self.background_color)
        self.diag_corner_img_rot_90 = pg.transform.rotate(self.diag_corner_img, 90)
        
        # Accessories images
        self.platform_img = pg.image.load("resources/graphics/platform.BMP").convert()
        self.platform_img.set_colorkey(self.background_color)
        self.platform_img_rot_90 = pg.transform.rotate(self.platform_img, 90)
        self.platform_img_rot_180 = pg.transform.rotate(self.platform_img, 180)
        self.platform_img_rot_270 = pg.transform.rotate(self.platform_img, 270)
        self.platform_images = {
            4: (self.platform_img, self.platform_img_rot_180),
            5: (self.platform_img_rot_90, self.platform_img_rot_270),
            6: self.platform_img,
            7: self.platform_img_rot_180,
            8: self.platform_img_rot_270,
            9: self.platform_img_rot_90,
        }
        
        # Dynamic variables
        self.file_type = FileTypes.NO
        self.state = MapStates.STANDARD
        self.map_pos_rect = pg.Rect(
            0,
            0,
            self.rect.width,
            self.rect.height)
        self.aspect_ratio = self.map_pos_rect.width / self.map_pos_rect.height
        self.px_ratio = self.map_pos_rect.width / self.rect.width
        self.loading_thickness = self.surf_size
        self.loading_rect = pg.Rect(0, 0, 0, 0)
        self.change_loading_rect_size()
        self.temp_surf = pg.Surface((self.rect.width * 3, self.rect.width * 3 / self.aspect_ratio))
        self.temp_rect = pg.Rect(
            self.temp_surf.get_width() // 2 - self.map_pos_rect.width // 2,
            self.temp_surf.get_height() // 2 - self.map_pos_rect.height // 2,
            self.map_pos_rect.width,
            self.map_pos_rect.height
        )
        self.tile_surf = pg.Surface((self.tile_size, self.tile_size))
        self.x_range = [float('inf'), float('-inf')]
        self.y_range = [float('inf'), float('-inf')]
        self.zoom_range = (self.rect.width, self.rect.width * 2.5)
        self.close_zoom_center = None
        self.close_zoom_dist = [0, 0]
        self.act_zoom_dist = [0, 0]
        self.total_zoom_change = None
        
    # Event management functions
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

    def start_moving_map(self,
                         event: pg.event.Event,
                         *args, **kwargs) -> bool:
        """
        Start moving map with left mousebuttondown
        :param event: pygame event
        :return: True: go to next event; False: go to next event handler
        """
        # Check mouse button
        if event.button != 1:
            return False
        # Check camera area
        if not self.rect.collidepoint(event.pos):
            return False
        # Start moving map
        self.state = MapStates.MOVE
        # Clear zoom center position
        self.close_zoom_center = None
        return True
    
    def moving_map_with_mouse(self,
                              event: pg.event.Event,
                              program,
                              ) -> bool:
        """
        Move map with left mousemotion
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event handler
        """
        # Check camera area
        if not self.rect.collidepoint(event.pos):
            return True
        self.move_map(
            x_move=event.rel[0] * self.px_ratio,
            y_move=event.rel[1] * self.px_ratio,
            program=program,
        )
        return True
        
    def move_map(self,
                 x_move: float,
                 y_move: float,
                 program,
                 ) -> None:
        """
        Move map. Notice x_move, y_move parameters inversed movement
        :param x_move: x movement multiplied with px_ratio
        :param y_move: y movement multiplied with px_ratio
        :param program: Program object
        """
        old_loading_x = self.loading_rect.x
        old_loading_y = self.loading_rect.y
        # Set new position
        new_x = int(self.map_pos_rect.x - x_move)
        if self.x_range[0] <= new_x + self.map_pos_rect.width and new_x <= self.x_range[1]:
            self.map_pos_rect.x = new_x
            self.loading_rect.x -= x_move
        new_y = int(self.map_pos_rect.y - y_move)
        if self.y_range[0] <= new_y + self.map_pos_rect.height and new_y <= self.y_range[1]:
            self.map_pos_rect.y = new_y
            self.loading_rect.y -= y_move
        # Check for need of loading
        # Horizontal
        old_surf_x = old_loading_x // self.surf_size * self.surf_size
        new_surf_x = self.loading_rect.x // self.surf_size * self.surf_size
        if old_surf_x != new_surf_x:
            # Moving to the left
            if old_surf_x > new_surf_x:
                # Load surfs on the left
                self.load_data(
                    x_end=old_surf_x - 1,
                )
                # Delete surfs on the right
                for surf_x in range(
                        self.loading_rect.right // self.surf_size * self.surf_size + self.surf_size,
                        max(self.surfs.keys()) + 1,
                        self.surf_size):
                    self.surfs.pop(surf_x)
            # Moving to the right
            else:
                # Load surfs on the right
                self.load_data(
                    x_start=old_loading_x + self.loading_rect.width + 1,
                )
                # Delete surfs on the left
                for surf_x in range(min(self.surfs.keys()), new_surf_x, self.surf_size):
                    self.surfs.pop(surf_x)
        # Vertical
        old_surf_y = old_loading_y // self.surf_size * self.surf_size
        new_surf_y = self.loading_rect.y // self.surf_size * self.surf_size
        if old_surf_y != new_surf_y:
            # Moving to the top
            if old_surf_y > new_surf_y:
                # Load surfs on the top
                self.load_data(
                    y_end=old_surf_y - 1,
                )
                # Delete surfs on the bottom
                surf_keys = list(self.surfs.keys())
                for surf_x in surf_keys:
                    try:
                        range_stop = max(self.surfs[surf_x].keys()) + 1
                    except ValueError:
                        self.surfs.pop(surf_x)
                        continue
                    for surf_y in range(
                            self.loading_rect.bottom // self.surf_size * self.surf_size + self.surf_size,
                            range_stop,
                            self.surf_size):
                        self.surfs[surf_x].pop(surf_y)
            # Moving to the bottom
            else:
                # Load surfs on the bottom
                self.load_data(
                    y_start=old_loading_y + self.loading_rect.height + 1,
                )
                # Delete surfs on the top
                surf_keys = list(self.surfs.keys())
                for surf_x in surf_keys:
                    try:
                        range_start = min(self.surfs[surf_x].keys())
                    except ValueError:
                        self.surfs.pop(surf_x)
                        continue
                    for surf_y in range(range_start, new_surf_y, self.surf_size):
                        self.surfs[surf_x].pop(surf_y)
        program.draw_rects.append(self.draw(surf=program.screen))
        
    def stop_moving_map(self,
                        event: pg.event.Event,
                        *args, **kwargs) -> bool:
        """
        Stop moving map with left mousebuttonup
        :param event: pygame event
        :return: True: go to next event; False: go to next event handler
        """
        # Check mouse button
        if event.button != 1:
            return False
        self.state = MapStates.STANDARD
        return True
    
    def standard_keydown(self,
                         event: pg.event.Event,
                         program,
                         ) -> bool:
        """
        Keydown event handler in standard state
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event handler
        """
        # Move map
        movers = {
            pg.K_LEFT: (self.tile_size, 0),
            pg.K_RIGHT: (-self.tile_size, 0),
            pg.K_UP: (0, self.tile_size),
            pg.K_DOWN: (0, -self.tile_size),
            pg.K_a: (self.tile_size, 0),
            pg.K_d: (-self.tile_size, 0),
            pg.K_w: (0, self.tile_size),
            pg.K_s: (0, -self.tile_size),
        }
        try:
            x_move, y_move = movers[event.key]
            
            self.move_map(
                x_move=x_move * self.px_ratio,
                y_move=y_move * self.px_ratio,
                program=program,
            )
            self.close_zoom_center = None
            return True
        except KeyError:
            pass
        # Zoom
        zoomers = {
            pg.K_q: 60,
            pg.K_e: -60,
        }
        try:
            self.zoom(
                program=program,
                zoom_rate=zoomers[event.key],
                is_mouse=False
            )
            return True
        except KeyError:
            return False
    
    def standard_mousemotion(self,
                             event: pg.event.Event,
                             program,
                             ) -> bool:
        """
        Mousemotion event handler in standard state
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event handler
        """
        if not self.rect.collidepoint(event.pos):
            return False
        # Get tile coordinate
        tile_x = ((event.pos[0] - self.rect.x) * self.px_ratio + self.map_pos_rect.x) // self.tile_size
        tile_y = ((event.pos[1] - self.rect.y) * self.px_ratio + self.map_pos_rect.y) // self.tile_size
        return True
    
    def standard_mousewheel(self,
                            event: pg.event.Event,
                            program,
                            ) -> bool:
        """
        Mousewheel event handler in standard state
        :param event: pygame event
        :param program: Program object
        :return: True: go to next event; False: go to next event handler
        """
        # Exclude horizontal wheeling
        if event.y == 0:
            return False
        # Exclude outside area
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return False
        # Zoom
        self.zoom(
            zoom_rate=event.y * -60,
            program=program
        )
        return True
    
    def zoom(self,
             program,
             zoom_rate: int,
             is_mouse: bool = True,
             ) -> None:
        """
        Zoom view
        :param program: Program object
        :param zoom_rate: rate of zoom
        :param is_mouse: Zoom with mouse wheel
        """
        # Zoom
        zoom_result = False
        if is_mouse:
            if self.zoom_with_mouse(zoom_rate=zoom_rate):
                zoom_result = True
        else:
            if self.zoom_with_key(zoom_rate=zoom_rate):
                zoom_result = True
                
        if not zoom_result:
            return
            
        # Set loading_rect
        old_surfs = {
            "x_start": self.loading_rect.left // self.surf_size * self.surf_size,
            "x_end": self.loading_rect.right // self.surf_size * self.surf_size,
            "y_start": self.loading_rect.top // self.surf_size * self.surf_size,
            "y_end": self.loading_rect.bottom // self.surf_size * self.surf_size
        }
        self.change_loading_rect_size(new_thickness=int(self.surf_size * self.px_ratio))
        new_surfs = {
            "x_start": self.loading_rect.left // self.surf_size * self.surf_size,
            "x_end": self.loading_rect.right // self.surf_size * self.surf_size,
            "y_start": self.loading_rect.top // self.surf_size * self.surf_size,
            "y_end": self.loading_rect.bottom // self.surf_size * self.surf_size
        }
        load_params = {
            "x_start": None,
            "x_end": None,
            "y_start": None,
            "y_end": None,
        }
        to_load = False
        for key in load_params.keys():
            if old_surfs[key] != new_surfs[key]:
                load_params[key] = new_surfs[key]
                to_load = True
        if to_load:
            self.load_data(**load_params)
        # Set temp_rect
        old_center = self.temp_rect.center
        self.temp_rect.width = self.map_pos_rect.width
        self.temp_rect.height = self.map_pos_rect.height
        self.temp_rect.center = old_center
        program.draw_rects.append(self.draw(surf=program.screen))
        
    def zoom_with_mouse(self, zoom_rate: int) -> bool:
        """
        Zoom with mouse
        :param zoom_rate: rate of zoom
        :return: True: zooming happened; False: zooming not happened
        """
        # Get parameters for zoom
        mouse_pos = pg.mouse.get_pos()
        rect_mouse_x = mouse_pos[0] - self.rect.x
        rect_mouse_y = mouse_pos[1] - self.rect.y
        map_pos_mouse_x = (rect_mouse_x * self.px_ratio) + self.map_pos_rect.x
        map_pos_mouse_y = (rect_mouse_y * self.px_ratio) + self.map_pos_rect.y
        # Set map_pos_rect size
        old_width = self.map_pos_rect.width
        old_center = self.map_pos_rect.center
        self.map_pos_rect.width += zoom_rate
        if self.map_pos_rect.width < self.zoom_range[0]:
            self.map_pos_rect.width = self.zoom_range[0]
        if self.map_pos_rect.width > self.zoom_range[1]:
            self.map_pos_rect.width = self.zoom_range[1]
        if old_width == self.map_pos_rect.width:
            return False
        self.map_pos_rect.height = self.map_pos_rect.width / self.aspect_ratio
        self.px_ratio = self.map_pos_rect.width / self.rect.width
        # Set map_pos_rect position
        # Zoom out
        if old_width < self.map_pos_rect.width:
            self.map_pos_rect.center = old_center
            self.close_zoom_center = None
        # Zoom in
        else:
            # Far zoom
            if self.map_pos_rect.width > self.zoom_range[1] / 2:
                self.map_pos_rect.x = map_pos_mouse_x - (rect_mouse_x * self.px_ratio)
                self.map_pos_rect.y = map_pos_mouse_y - (rect_mouse_y * self.px_ratio)
            # Close zoom
            else:
                if self.close_zoom_center is None:
                    self.close_zoom_center = (map_pos_mouse_x, map_pos_mouse_y)
                    self.close_zoom_dist[0] = mouse_pos[0] - self.rect.centerx
                    self.close_zoom_dist[1] = mouse_pos[1] - self.rect.centery
                    self.act_zoom_dist[0] = mouse_pos[0] - self.rect.centerx
                    self.act_zoom_dist[1] = mouse_pos[1] - self.rect.centery
                    self.total_zoom_change = (old_width - self.zoom_range[0]) / self.zoom_range[0]
                old_zoom = (old_width - self.zoom_range[0]) / self.zoom_range[0]
                new_zoom = (self.map_pos_rect.width - self.zoom_range[0]) / self.zoom_range[0]
                act_zoom_change = (old_zoom - new_zoom) / self.total_zoom_change
                self.act_zoom_dist[0] -= self.close_zoom_dist[0] * act_zoom_change
                self.act_zoom_dist[1] -= self.close_zoom_dist[1] * act_zoom_change
                self.map_pos_rect.center = self.close_zoom_center
                self.map_pos_rect.centerx -= self.act_zoom_dist[0] * self.px_ratio
                self.map_pos_rect.centery -= self.act_zoom_dist[1] * self.px_ratio
            # Check position out of range
            if self.map_pos_rect.right < self.x_range[0]:
                self.map_pos_rect.right = self.x_range[0]
            elif self.map_pos_rect.left > self.x_range[1]:
                self.map_pos_rect.left = self.x_range[1]
            if self.map_pos_rect.bottom < self.y_range[0]:
                self.map_pos_rect.bottom = self.y_range[0]
            elif self.map_pos_rect.top > self.y_range[1]:
                self.map_pos_rect.top = self.y_range[1]
        return True
                
    def zoom_with_key(self, zoom_rate: int) -> bool:
        """
        Zoom with keys
        :param zoom_rate: rate of zoom
        :return: True: zooming happened; False: zooming not happened
        """
        # Set map_pos_rect size
        old_width = self.map_pos_rect.width
        old_center = self.map_pos_rect.center
        self.map_pos_rect.width += zoom_rate
        if self.map_pos_rect.width < self.zoom_range[0]:
            self.map_pos_rect.width = self.zoom_range[0]
        if self.map_pos_rect.width > self.zoom_range[1]:
            self.map_pos_rect.width = self.zoom_range[1]
        if old_width == self.map_pos_rect.width:
            return False
        self.map_pos_rect.height = self.map_pos_rect.width / self.aspect_ratio
        self.px_ratio = self.map_pos_rect.width / self.rect.width
        # Set map_pos_rect position
        self.map_pos_rect.center = old_center
        self.close_zoom_center = None
        return True
        
    # Data and rect management functions
    def change_loading_rect_size(self,
                                 new_thickness: int = None,
                                 ) -> None:
        """
        Change size of loading rect
        :param new_thickness: thickness of loading rect relative to map rect
        """
        if new_thickness is not None:
            self.loading_thickness = new_thickness
        self.loading_rect.x = self.map_pos_rect.x - self.loading_thickness
        self.loading_rect.y = self.map_pos_rect.y - self.loading_thickness
        self.loading_rect.width = self.map_pos_rect.width + (self.loading_thickness * 2)
        self.loading_rect.height = self.map_pos_rect.height + (self.loading_thickness * 2)
        
    def load_data(self,
                  x_start: int = None,
                  x_end: int = None,
                  y_start: int = None,
                  y_end: int = None,
                  ) -> None:
        """
        Load data from map database. If none of the parameters are given, than it loads data for whole loading area.
        :param x_start: start of x range to load (inclusive)
        :param x_end: end of x range to load (inclusive)
        :param y_start: start of y range to load (inclusive)
        :param y_end: end of y range to load (inclusive)
        """
        # Get the area to load
        is_None = [False, False, False, False]
        if x_start is None:
            x_start = self.loading_rect.left
            is_None[0] = True
        if x_end is None:
            x_end = self.loading_rect.right
            is_None[1] = True
        if y_start is None:
            y_start = self.loading_rect.top
            is_None[2] = True
        if y_end is None:
            y_end = self.loading_rect.bottom
            is_None[3] = True
        if False not in is_None:
            self.surfs.clear()
        surf_x_start = x_start // self.surf_size * self.surf_size
        surf_x_end = x_end // self.surf_size * self.surf_size
        surf_y_start = y_start // self.surf_size * self.surf_size
        surf_y_end = y_end // self.surf_size * self.surf_size
        # Create small surfaces & draw content onto them
        for surf_x in range(surf_x_start, surf_x_end + 1, self.surf_size):
            if surf_x not in self.surfs.keys():
                self.surfs[surf_x] = {}
            for surf_y in range(surf_y_start, surf_y_end + 1, self.surf_size):
                if surf_y in self.surfs[surf_x].keys():
                    continue
                self.create_surf(
                    surf_x=surf_x,
                    surf_y=surf_y,
                )
                
        # Set limits -- only at first load
        if False in is_None:
            return
        self.x_range[0] = min(self.map.data.keys()) * self.tile_size + self.tile_size
        self.x_range[1] = max(self.map.data.keys()) * self.tile_size
        self.y_range[0] = float('inf')
        self.y_range[1] = float('-inf')
        for data_x in self.map.data.values():
            min_y = min(data_x.keys())
            if min_y < self.y_range[0]:
                self.y_range[0] = min_y
            max_y = max(data_x.keys())
            if max_y > self.y_range[1]:
                self.y_range[1] = max_y
        self.y_range[0] *= self.tile_size
        self.y_range[0] += self.tile_size
        self.y_range[1] *= self.tile_size
        
    def set_default(self, new_file_type: int):
        """
        Clear all graphic data and set dynamic variables to default
        """
        self.change_file_type(new_file_type=new_file_type)
        self.surfs.clear()
        self.state = MapStates.STANDARD
        self.map_pos_rect = pg.Rect(
            0,
            0,
            self.rect.width,
            self.rect.height)
        self.loading_thickness = self.surf_size
        self.change_loading_rect_size()
        self.temp_surf = pg.Surface(self.loading_rect.size)
        self.temp_rect = pg.Rect(
            self.temp_surf.get_width() // 2 - self.map_pos_rect.width // 2,
            self.temp_surf.get_height() // 2 - self.map_pos_rect.height // 2,
            self.map_pos_rect.width,
            self.map_pos_rect.height
        )
        self.tile_surf = pg.Surface((self.tile_size, self.tile_size))
        self.x_range = [float('inf'), float('-inf')]
        self.y_range = [float('inf'), float('-inf')]
        self.zoom_scale = 1
        
    def create_surf(self,
                    surf_x: int,
                    surf_y: int,
                    ) -> None:
        """
        Create small surface and draw content
        :param surf_x: x position of surface left
        :param surf_y: y position of surface top
        """
        # Create surf
        self.surfs[surf_x][surf_y] = pg.Surface(
            size=(
                self.surf_size,
                self.surf_size
            ),
        )
        # Draw standard background
        self.surfs[surf_x][surf_y].fill(self.background_color)
        # Draw tiles
        for coord_x in range(
                surf_x // self.tile_size,
                (surf_x + self.surf_size) // self.tile_size,
                1):
            try:
                self.map.data[coord_x]
            except KeyError:
                continue
            for coord_y in range(
                    surf_y // self.tile_size,
                    (surf_y + self.surf_size) // self.tile_size,
                    1):
                try:
                    self.map.data[coord_x][coord_y]
                except KeyError:
                    continue
                self.draw_tile(
                    coord_x=coord_x,
                    coord_y=coord_y,
                    surf=self.surfs[surf_x][surf_y],
                )
              
    # Draw functions
    def draw_tile(self,
                  coord_x: int,
                  coord_y: int,
                  surf: pg.Surface,
                  ) -> None:
        """
        Draw tile on map surface
        :param coord_x: map coordinate x
        :param coord_y: map coordinate y
        :param surf: small surface the tile will be drawn onto
        """
        data_arr = self.map.data[coord_x][coord_y]
        tile_x = coord_x % self.tile_count_surf * self.tile_size
        tile_y = coord_y % self.tile_count_surf * self.tile_size
        selector = data_arr[0]
        draw_functs = (
            self.draw_platform_terrain,
            self.draw_rail,
            self.draw_rail,
            self.draw_fence,
            self.draw_fence,
            self.draw_misc,
        )
        self.tile_surf.fill(self.background_color)
        data_idx = 1
        for bit_idx in range(8):
            if not (selector >> bit_idx) & 1:
                continue
            draw_functs[bit_idx](
                data=data_arr[data_idx],
            )
            data_idx += 1
        surf.blit(self.tile_surf, (tile_x, tile_y))
        
    def draw_rail(self, data: int) -> None:
        """
        Draw rail image on tile
        :param data: rail code
        """
        self.tile_surf.blit(self.rail_image_codes[data], (0, 0))
        
    def draw_platform_terrain(self, data: int) -> None:
        """
        Draw platform and/or terrain on tile
        :param data: platform/terrain code
        """
        # Draw terrain
        terrain_code = data
        if data > 99:
            terrain_code = terrain_code % 10
            
        self.tile_surf.fill(self.terrain_codes[terrain_code])
        # Draw platform
        if data // 100 == 0:
            return
        platform_code = data % 100 // 10
        if platform_code < 6:
            for i in range(2):
                self.tile_surf.blit(self.platform_images[platform_code][i], (0, 0))
        else:
            self.tile_surf.blit(self.platform_images[platform_code], (0, 0))
        
    
    def draw_fence(self, data: int) -> None:
        """
        Draw fence on tile
        :param data: fence code
        """
        return
    
    def draw_misc(self, data: int) -> None:
        """
        Draw miscellaneous
        :param data: miscellaneous code
        """
        return
    
    def change_file_type(self,
                         new_file_type: int,
                         ) -> None:
        """
        Change file type
        :param new_file_type: file type code
        """
        self.file_type = new_file_type
        
    def draw_temp_surface(self):
        """
        Draw all loaded small surfaces onto temporary surface
        """
        for surf_x in self.surfs.keys():
            for surf_y, map_surf in self.surfs[surf_x].items():
                self.temp_surf.blit(
                    source=map_surf,
                    dest=(
                        (surf_x - self.map_pos_rect.left) + self.temp_rect.left,
                        (surf_y - self.map_pos_rect.top) + self.temp_rect.top
                    ),
                )
        
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw map view image on surface
        :param surf: surface drawn onto
        :return rect area to draw
        """
        # Draw onto temporary surface
        self.draw_temp_surface()
        # Create scaled surface
        to_scale_surf = pg.Surface(self.temp_rect.size)
        to_scale_surf.blit(
            source=self.temp_surf,
            dest=(0, 0),
            area=self.temp_rect,
        )
        scaled_surf = pg.transform.scale(to_scale_surf, self.rect.size)
        # Draw temporary surface area to main surface
        surf.blit(
            source=scaled_surf,
            dest=self.rect,
        )
        return self.rect
    
    # Resizing functions
    def change_size(self,
                    new_size: tuple):
        """
        Update camera view basic size and reset map rectangle area
        :param new_size: new size of background (width, height)
        """
        change_rate = new_size[0] / self.rect.width
        # Update rect
        self.rect = pg.Rect(
            self.rect.topleft,
            new_size
        )
        # Update dynamic rects
        self.map_pos_rect = pg.Rect(
            self.map_pos_rect.centerx - self.rect.width // 2,
            self.map_pos_rect.centery - self.rect.height // 2,
            self.map_pos_rect.width * change_rate,
            self.map_pos_rect.height * change_rate
        )
        self.px_ratio = self.map_pos_rect.width / self.rect.width
        self.zoom_range = (self.rect.width, self.rect.width * 2.5)
        self.change_loading_rect_size()
        # Check position out of range
        if self.map_pos_rect.right < self.x_range[0]:
            self.map_pos_rect.right = self.x_range[0]
        elif self.map_pos_rect.left > self.x_range[1]:
            self.map_pos_rect.left = self.x_range[1]
        if self.map_pos_rect.bottom < self.y_range[0]:
            self.map_pos_rect.bottom = self.y_range[0]
        elif self.map_pos_rect.top > self.y_range[1]:
            self.map_pos_rect.top = self.y_range[1]
        # Update temp surf&rects
        self.temp_surf = pg.Surface((self.zoom_range[1], self.zoom_range[1] / self.aspect_ratio))
        self.temp_rect = pg.Rect(
            self.temp_surf.get_width() // 2 - self.map_pos_rect.width // 2,
            self.temp_surf.get_height() // 2 - self.map_pos_rect.height // 2,
            self.map_pos_rect.width,
            self.map_pos_rect.height
        )
        # Reload data
        if self.file_type != FileTypes.NO:
            self.load_data(
                x_start=self.loading_rect.left,
                x_end=self.loading_rect.right,
                y_start=self.loading_rect.top,
                y_end=self.loading_rect.bottom
            )
        