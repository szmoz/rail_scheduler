from datetime import datetime
import os
import pygame as pg

from code.util.event_manager import EventManager
from code.util.frame import Frame
from code.util.text import Text

from code.window.color_data import FileColors as C
from code.window.string_data import FileStrings
from code.window.variable_data import FILE_DIR_PATHS, FILE_EXTENSIONS


class FileNameList:
    """
    Scrollable list with file data (name, size, creation date, modification date)
    """
    def __init__(self,
                 rect: pg.Rect,
                 frame_thickness: int,
                 frame_top_color: tuple,
                 frame_bottom_color: tuple,
                 frame_edge_lines: tuple,
                 text_size: int,
                 text_type: str,
                 file_type: int,
                 ) -> None:
        """
        Initialize FileNameList object
        :param rect: rectangle area of object
        :param frame_thickness: frame thickness
        :param frame_top_color: frame top&left color
        :param frame_bottom_color: frame bottom&right color
        :param frame_edge_lines: frame edge line codes
        :param text_size: size of text
        :param text_type: path to text type (.ttf)
        :param file_type: type of files to list
        """
        # Data
        self.dir_path = FILE_DIR_PATHS[file_type]
        self.extension = FILE_EXTENSIONS[file_type]
        files = []
        for file in os.listdir(f"{self.dir_path}/"):
            if not file.endswith(self.extension):
                continue
            size = os.path.getsize(f"{self.dir_path}/{file}") // 1024
            create_time = os.path.getctime(f"{self.dir_path}/{file}")
            mod_time = os.path.getmtime(f"{self.dir_path}/{file}")
            files.append({
                'name': file.rstrip(self.extension),
                'size': str(size) + " KB",
                'create_time': datetime.fromtimestamp(create_time).strftime('%Y.%m.%d. %H:%M'),
                'mod_time': datetime.fromtimestamp(mod_time).strftime('%Y.%m.%d. %H:%M'),
            })
            
        # Visible Surface content
        self.element_height = text_size + 4
        self.rect = rect
        # Frame
        self.frame = Frame(
            rect=rect,
            thickness=frame_thickness,
            top_color=frame_top_color,
            bottom_color=frame_bottom_color,
            edge_lines=frame_edge_lines,
        )
        # List rect
        self.list_rect = pg.Rect(
            rect.left + frame_thickness,
            rect.top + frame_thickness + self.element_height,
            rect.width - (frame_thickness * 2),
            rect.height - (frame_thickness * 2) - self.element_height,
        )
        self.n_visible = self.list_rect.height // self.element_height
        
        # List Surface
        surface_height = self.element_height * len(files)
        if surface_height < self.list_rect.height:
            surface_height = self.list_rect.height
        self.list = pg.Surface(
            size=(
                self.list_rect.width,
                surface_height,
            ),
        )
        self.list.fill(C.LIST_BACKGROUND)
        # Dividing lines
        self.lines = []
        for i in range(3):
            self.lines.append(pg.Rect(
                (self.list_rect.width // 2) + (self.list_rect.width // 2 // 3 * i),
                0,
                1,
                self.list.get_size()[1],
            ))
        widths = []
        rights = [0]
        for line in self.lines:
            pg.draw.rect(
                surface=self.list,
                color=C.LIST_LINE,
                rect=line,
            )
            widths.append(line.left - rights[-1])
            rights.append(line.right)
        widths.append(self.list_rect.width - rights[-1])
        # Elements
        data_types = ('name', 'size', 'create_time', 'mod_time')
        self.texts = []
        idx = 0
        for i in range(len(files)):
            name_text = Text(
                text=files[i][data_types[0]],
                text_type=text_type,
                size=text_size,
                color=C.LIST_TEXT,
                anchor_type='midleft',
                anchor_pos=(
                    frame_thickness,
                    idx * self.element_height + (self.element_height // 2),
                ),
            )
            if name_text.rect.width > widths[0] - (frame_thickness * 8):
                continue
            else:
                self.texts.append([])
                self.texts[idx].append(name_text)
            for j in range(1, len(data_types)):
                self.texts[idx].append(Text(
                    text=files[i][data_types[j]],
                    text_type=text_type,
                    size=text_size,
                    color=C.LIST_TEXT,
                    anchor_type='midleft',
                    anchor_pos=(
                        rights[j] + frame_thickness,
                        idx * self.element_height + (self.element_height // 2),
                    ),
                ))
            idx += 1
                
        for line in self.texts:
            for text in line:
                text.draw(self.list)
                
        # Title
        # Text
        self.title = []
        for i in range(len(widths)):
            self.title.append(pg.sprite.Sprite())
            self.title[-1].image = pg.Surface(
                size=(
                    widths[i],
                    self.element_height,
                ),
            )
            self.title[-1].image.fill(C.LIST_TITLE_BACKGROUND)
            text = Text(
                text=FileStrings.LIST_TITLE_TEXTS[i],
                text_type=text_type,
                size=text_size,
                color=C.LIST_TEXT,
                anchor_type='midleft',
                anchor_pos=(
                    frame_thickness,
                    self.element_height // 2,
                ),
            )
            text.draw(self.title[-1].image)
            self.title[-1].rect = self.title[-1].image.get_rect()
            self.title[-1].rect.left = self.list_rect.left + rights[i]
            self.title[-1].rect.bottom = self.list_rect.top
        # Arrow
        pg.draw.polygon(
            surface=self.title[0].image,
            color=C.LIST_TITLE_ARROW,
            points=(
                (self.title[0].rect.width - (frame_thickness * 2),
                 (frame_thickness * 2)),
                (self.title[0].rect.width - (frame_thickness * 2) - (self.title[0].rect.height - (frame_thickness * 4)),
                 (frame_thickness * 2)),
                (self.title[0].rect.width - (frame_thickness * 2) - ((self.title[0].rect.height - (frame_thickness * 4)) // 2),
                 self.title[0].rect.height - (frame_thickness * 2)),
            ),
        )
        
        # Event management
        self.standard_event_manager = EventManager(
                event_types=(pg.MOUSEBUTTONDOWN, pg.MOUSEWHEEL, pg.KEYDOWN),
                event_functions=(self.isclicked, self.isrolled, self.keydown),
            )
        
        # Dynamic variables
        self.top_el_idx = 0
        self.clicked_idx = -1
        self.sort = 1
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      file_win,
                      ) -> bool:
        """
        Event manager for FileNameList
        :param event: pygame Event
        :param program: Program object
        :param file_win: FileWindow object
        :return: True: go to next event; False: go to next event manager
        """
        event_result = self.standard_event_manager.handle(
            event=event,
            program=program,
        )
        update_textbox_event_types = (pg.MOUSEBUTTONDOWN, pg.KEYDOWN)
        if event_result and event.type in update_textbox_event_types:
            self.update_textbox(program, file_win)
        return event_result
    
    def isclicked(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        Check if list element is clicked
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Check for object rectangle area click
        if not self.rect.collidepoint(event.pos):
            return False
        # Check for title click
        if not self.list_rect.collidepoint(event.pos):
            for title_idx in range(len(self.title)):
                if self.title[title_idx].rect.collidepoint(event.pos):
                    self.sorting(
                        column_idx=title_idx,
                        program=program,
                    )
                    return True
            return False
        # List area click
        el_idx = (event.pos[1] - self.list_rect.top) // self.element_height + self.top_el_idx
        # Click in empty element
        if el_idx >= len(self.texts):
            if self.clicked_idx < 0:
                return False
            program.draw_rects.append(self.update_list(program.screen, new_clicked_idx=-1))
            return True
        # Element click
        program.draw_rects.append(self.update_list(program.screen, new_clicked_idx=el_idx))
        return True
    
    def isrolled(self,
                 event: pg.event.Event,
                 program,
                 ) -> bool:
        """
        Check if list is rolled
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        if not self.list_rect.collidepoint(pg.mouse.get_pos()):
            return False
        if event.y < 0:
            self.roll_down(event, program)
            return True
        elif event.y > 0:
            self.roll_up(event, program)
            return True
        return False
    
    def roll_down(self,
                  event: pg.event.Event,
                  program,
                  ) -> None:
        """
        Roll list down
        :param event: pygame event
        :param program: Program object
        """
        try:
            diff = abs(event.y)
        except AttributeError:
            diff = 1
        old_top_el_idx = self.top_el_idx
        self.top_el_idx = min(
            len(self.texts) - self.n_visible,
            self.top_el_idx + diff,
        )
        if old_top_el_idx == self.top_el_idx:
            return
        program.draw_rects.append(self.draw_list(program.screen))
    
    def roll_up(self,
                event: pg.event.Event,
                program,
                ) -> None:
        """
        Roll list up
        :param event: pygame event
        :param program: Program object
        """
        try:
            diff = event.y
        except AttributeError:
            diff = 1
        old_top_el_idx = self.top_el_idx
        self.top_el_idx = max(
            0,
            self.top_el_idx - diff,
        )
        if old_top_el_idx == self.top_el_idx:
            return
        program.draw_rects.append(self.draw_list(program.screen))
    
    def keydown(self,
                event: pg.event.Event,
                program,
                ) -> bool:
        """
        Keydown event function
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        keys = (pg.K_DOWN, pg.K_UP)
        if event.key not in keys:
            return False
        key_functs = {
            pg.K_DOWN: self.step_down,
            pg.K_UP: self.step_up}
        key_functs[event.key](program=program)
        return True
    
    def step_down(self,
                  program,
                  ) -> None:
        """
        Step down by one
        :param program: Program object
        """
        if self.clicked_idx == len(self.texts) - 1:
            return
        if self.clicked_idx < 0:
            new_clicked_idx = 1
        else:
            new_clicked_idx = self.clicked_idx + 1
        program.draw_rects.append(self.update_list(
            surf=program.screen,
            new_clicked_idx=new_clicked_idx,
        ))
    
    def step_up(self,
                program,
                ) -> None:
        """
        Step up by one
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        if self.clicked_idx <= 0:
            return
        program.draw_rects.append(self.update_list(
            surf=program.screen,
            new_clicked_idx=self.clicked_idx - 1,
        ))
        
    def find_name(self,
                  name: str,
                  ) -> int:
        """
        Find name in file names
        :param name: name to fund
        :return: index of element
        """
        for i in range(len(self.texts)):
            if self.texts[i][0].text == name:
                return i
        return -1
    
    def draw_list(self,
                  surf: pg.Surface,
                  ) -> pg.Rect:
        """
        Draw list area
        :param surf: surface
        :return: rectangle area for draw_rect list
        """
        surf.blit(source=self.list,
                  dest=self.list_rect,
                  area=pg.Rect(
                      (0,
                       self.top_el_idx * self.element_height),
                      self.list_rect.size
                  ))
        return self.list_rect
    
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw FileNameList object
        :param surf: surface
        :return: rectangle area for draw_rect list
        """
        # Frame
        self.frame.draw(surf)
        # Title
        for title in self.title:
            surf.blit(title.image, title.rect)
        # List
        self.draw_list(surf)
        return self.rect
        
    def update_list(self,
                    surf: pg.Surface,
                    new_clicked_idx: int = None,
                    ) -> pg.Rect:
        """
        Change clicked background and redraw
        :param new_clicked_idx: new text
        :param surf: surface
        :return rect area to draw
        """
        if new_clicked_idx is None:
            new_clicked_idx = -1
        # Unclick clicked element
        if self.clicked_idx >= 0:
            pg.draw.rect(
                surface=self.list,
                color=C.LIST_BACKGROUND,
                rect=pg.Rect(
                    0,
                    self.clicked_idx * self.element_height,
                    self.list_rect.width,
                    self.element_height,
                ),
            )
            for text in self.texts[self.clicked_idx]:
                text.draw(self.list)
        # Click new element
        self.clicked_idx = new_clicked_idx
        if self.clicked_idx >= 0:
            pg.draw.rect(
                surface=self.list,
                color=C.LIST_BACKGROUND_CLICKED,
                rect=pg.Rect(
                    0,
                    self.clicked_idx * self.element_height,
                    self.list_rect.width,
                    self.element_height,
                ),
            )
            for text in self.texts[self.clicked_idx]:
                text.draw(self.list)
            if self.clicked_idx < self.top_el_idx:
                self.top_el_idx = self.clicked_idx
            elif self.clicked_idx > self.top_el_idx + self.n_visible - 1:
                self.top_el_idx = self.clicked_idx - self.n_visible + 1
                if self.top_el_idx > len(self.texts) - self.n_visible:
                    self.top_el_idx = len(self.texts) - self.n_visible
        # Draw lines
        for line in self.lines:
            pg.draw.rect(
                surface=self.list,
                color=C.LIST_LINE,
                rect=line,
            )
        
        # Redraw
        self.draw_list(surf)
        return self.list_rect
    
    def sorting(self,
                column_idx: int,
                program,
                ) -> None:
        """
        Sort list according to selected column
        :param column_idx: column index
        :param program: Program object
        """
        old_sort = self.sort
        # Set new sort rule
        new_sort = column_idx + 1
        if new_sort == self.sort:
            self.sort *= -1
        else:
            self.sort = new_sort
        # Clear previous arrow
        pg.draw.rect(
            surface=self.title[abs(old_sort) - 1].image,
            color=C.LIST_TITLE_BACKGROUND,
            rect=pg.Rect(
                self.title[abs(old_sort) - 1].rect.width - self.title[abs(old_sort) - 1].rect.height,
                0,
                self.title[abs(old_sort) - 1].rect.height,
                self.title[abs(old_sort) - 1].rect.height
            ),
        )
        if abs(old_sort) != new_sort:
            program.screen.blit(
                self.title[abs(old_sort) - 1].image,
                self.title[abs(old_sort) - 1].rect,
            )
            program.draw_rects.append(self.title[abs(old_sort) - 1].rect)
        # Draw new arrow
        if self.sort > 0:
            arrow_points = (
                (self.title[column_idx].rect.width - (self.frame.thickness * 2),
                 self.frame.thickness * 2),
                (self.title[column_idx].rect.width - (self.frame.thickness * 2) -
                 (self.title[column_idx].rect.height - (self.frame.thickness * 4)),
                 self.frame.thickness * 2),
                (self.title[column_idx].rect.width - (self.frame.thickness * 2) -
                 ((self.title[column_idx].rect.height - (self.frame.thickness * 4)) // 2),
                 self.title[column_idx].rect.height - (self.frame.thickness * 2)),
            )
        else:
            arrow_points = (
                (self.title[column_idx].rect.width - (self.frame.thickness * 2),
                 self.title[column_idx].rect.height - (self.frame.thickness * 2)),
                (self.title[column_idx].rect.width - (self.frame.thickness * 2) -
                 (self.title[column_idx].rect.height - (self.frame.thickness * 4)),
                 self.title[column_idx].rect.height - (self.frame.thickness * 2)),
                (self.title[column_idx].rect.width - (self.frame.thickness * 2) -
                 ((self.title[column_idx].rect.height - (self.frame.thickness * 4)) // 2),
                 self.frame.thickness * 2),
            )
        pg.draw.polygon(
            surface=self.title[column_idx].image,
            color=C.LIST_TITLE_ARROW,
            points=arrow_points,
        )
        program.screen.blit(
            self.title[column_idx].image,
            self.title[column_idx].rect,
        )
        program.draw_rects.append(self.title[column_idx].rect)
        if self.clicked_idx >= 0:
            clicked_name = self.texts[self.clicked_idx][0]
        # Sort data
        def sort_ascending():
            for i in range(len(self.texts) - 1, 0, -1):
                for j in range(0, i):
                    if self.texts[j + 1][column_idx].text < self.texts[j][column_idx].text:
                        temp = self.texts[j]
                        self.texts[j] = self.texts[j + 1]
                        self.texts[j + 1] = temp
                        for t in self.texts[j]:
                            t.rect.y -= self.element_height
                        for t in self.texts[j + 1]:
                            t.rect.y += self.element_height
        
        def sort_descending():
            for i in range(len(self.texts) - 1, 0, -1):
                for j in range(len(self.texts) - 1, len(self.texts) - i - 1, -1):
                    if self.texts[j - 1][column_idx].text < self.texts[j][column_idx].text:
                        temp = self.texts[j]
                        self.texts[j] = self.texts[j - 1]
                        self.texts[j - 1] = temp
                        for t in self.texts[j]:
                            t.rect.y += self.element_height
                        for t in self.texts[j - 1]:
                            t.rect.y -= self.element_height
        
        if self.sort < 0:
            sort_descending()
        else:
            sort_ascending()
        
        # Draw list
        # Background
        self.list.fill(C.LIST_BACKGROUND)
        # Clicked element
        if self.clicked_idx >= 0:
            for i in range(len(self.texts)):
                if self.texts[i][0] == clicked_name:
                    print(i)
                    self.clicked_idx = i
                    break
            pg.draw.rect(
                surface=self.list,
                color=C.LIST_BACKGROUND_CLICKED,
                rect=pg.Rect(
                    0,
                    self.clicked_idx * self.element_height,
                    self.list_rect.width,
                    self.element_height,
                ),
            )
            if self.clicked_idx < self.top_el_idx:
                self.top_el_idx = self.clicked_idx
            elif self.clicked_idx > self.top_el_idx + self.n_visible - 1:
                self.top_el_idx = self.clicked_idx - self.n_visible + 1
                if self.top_el_idx > len(self.texts) - self.n_visible:
                    self.top_el_idx = len(self.texts) - self.n_visible
        # Texts
        for line in self.texts:
            for text in line:
                text.draw(self.list)
        program.draw_rects.append(self.draw_list(program.screen))
    
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
        self.frame.reposition(x_diff, y_diff)
        self.list_rect.x += x_diff
        self.list_rect.y += y_diff
        for title in self.title:
            title.rect.x += x_diff
            title.rect.y += y_diff
        
    def update_textbox(self,
                       program,
                       file_win,
                       ) -> None:
        """
        Update textbox if element is clicked
        :param program: Program object
        :param file_win: FileWindow object
        """
        if self.clicked_idx < 0:
            file_win.textbox.unhighlight(
                program=program
            )
            return
        file_win.textbox.change_text_highlight_all(
            new_text=self.texts[self.clicked_idx][0].text,
            program=program
        )
        