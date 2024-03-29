import pygame as pg

from code.util.background import Background
from code.util.colors import Colors as C
from code.util.event_manager import EventManager
from code.util.frame import Frame
from code.util.text import Text
from code.util.states import TextBoxStates as States
from code.util.variable_data import CustomUserEvents


class TextBox:
    """
    Textbox object with editable text
    """
    def __init__(self,
                 rect: pg.Rect,
                 frame_thickness: int,
                 frame_top_color: tuple,
                 frame_bottom_color: tuple,
                 frame_edge_lines: tuple,
                 text_size: int,
                 text_type: str,
                 align: str,
                 start_text: str = None,
                 ) -> None:
        """
        Initialize TextBox object
        :param rect: rectangle area of object
        :param frame_thickness: frame thickness
        :param frame_top_color: frame top&left color
        :param frame_bottom_color: frame bottom&right volor
        :param frame_edge_lines: frame edge line codes
        :param start_text: starting text
        :param text_size: size of text
        :param text_type: path to text type (.ttf)
        :param align: "left" or "right" alignment
        """
        # Surface content
        # Background
        self.background = Background(
            rect=pg.Rect(
                rect.left + frame_thickness,
                rect.top + frame_thickness,
                rect.width - (frame_thickness * 2),
                rect.height - (frame_thickness * 2),
            ),
            color=C.WHITE,
        )
        # Frame
        self.frame = Frame(
            rect=rect,
            thickness=frame_thickness,
            top_color=frame_top_color,
            bottom_color=frame_bottom_color,
            edge_lines=frame_edge_lines,
        )
        # Rect
        self.rect = rect
        # Text
        self.max_text_length = self.background.rect.width - (self.frame.thickness * 8)
        if start_text is None:
            start_text = ""
        anchor_positions = (
            (self.background.rect.left + frame_thickness, rect.centery),
            (self.background.rect.right - frame_thickness, rect.centery))
        anchor_types = ("left", "right")
        anchor_pos = None
        for i in range(len(anchor_types)):
            if align == anchor_types[i]:
                anchor_pos = anchor_positions[i]
                break
        self.text = Text(
            text=start_text,
            text_type=text_type,
            size=text_size,
            color=C.BLACK,
            anchor_type="mid" + align,
            anchor_pos=anchor_pos,
        )
        
        # Data
        self.highlight_color = C.LIGHTER_BLUE
        self.highlight_top = self.background.rect.top + frame_thickness
        self.highlight_height = self.background.rect.height - (frame_thickness * 2)
        
        # Event management
        self.event_managers = {
            States.STANDARD: EventManager(
                event_types=(pg.MOUSEBUTTONDOWN, ),
                event_functions=(self.isclicked, ),
            ),
            States.CURSOR: EventManager(
                event_types=(
                    CustomUserEvents.CURSOR_SWITCH,
                    pg.MOUSEBUTTONDOWN,
                    pg.TEXTINPUT,
                    pg.KEYDOWN,
                ),
                event_functions=(
                    self.switch_cursor,
                    self.isclicked,
                    self.textinput,
                    self.keydown,
                ),
            ),
            States.HIGHLIGHTING: EventManager(
                event_types=(
                    pg.MOUSEMOTION,
                    pg.MOUSEBUTTONUP,
                ),
                event_functions=(
                    self.highlighting,
                    self.stop_highlighting,
                ),
            ),
            States.HIGHLIGHTED: EventManager(
                event_types=(pg.MOUSEBUTTONDOWN,
                             pg.KEYDOWN,
                             pg.TEXTINPUT,
                             ),
                event_functions=(
                    self.isclicked,
                    self.highlight_keydown,
                    self.highlight_textinput,
                ),
            ),
        }
        
        # Dynamic variables
        self.char_mid_pos = []
        self.char_end_pos = []
        self.update_char_positions()
        self.cursor_pos = -1
        self.cursor_state = False
        self.highlight_ends = [-1, -1]
        self.state = States.STANDARD

        # Cursor rect
        self.cursor_rect = pg.Rect(
            self.char_end_pos[0],
            self.highlight_top,
            1,
            self.highlight_height,
        )
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      ) -> bool:
        """
        Event manager for textbox
        :param event: pygame Event
        :param program: Program object
        :return: True: go to next event; False: go to next event manager
        """
        #print(event)
        return self.event_managers[self.state].handle(
            event=event,
            program=program
        )
    
    def isclicked(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        Check if mouse clicked in text area
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Click outside of text area
        if not self.background.rect.collidepoint(event.pos):
            if self.state == States.CURSOR:
                self.state = States.STANDARD
                self.deactivate_cursor(program)
            return False
        # Click in text area - start highlighting
        if self.state == States.CURSOR:
            self.deactivate_cursor(program)
        self.state = States.HIGHLIGHTING
        self.highlight_ends[0] = self.get_mouse_pos_in_text(
            mouse_x=event.pos[0],
        )
        self.highlight_ends[1] = -1
        program.draw_rects.append(self.draw_text(program.screen))
        return True
    
    def activate_cursor(self,
                        program,
                        new_cursor_pos: int = None,
                        ) -> None:
        """
        Activate cursor
        :param program: Program object
        :param new_cursor_pos: new cursor position (char index)
        """
        if new_cursor_pos is not None:
            self.move_cursor(
                new_cursor_pos=new_cursor_pos,
            )
        self.cursor_state = False
        if pg.event.peek(CustomUserEvents.CURSOR_SWITCH):
            pg.event.clear(CustomUserEvents.CURSOR_SWITCH)
        self.switch_cursor(program=program)
        
    def deactivate_cursor(self,
                          program,
                          ) -> None:
        """
        Deactivate cursor
        :param program: Program object
        """
        self.cursor_state = False
        self.cursor_pos = -1
        pg.event.clear(CustomUserEvents.CURSOR_SWITCH)
        program.draw_rects.append(self.draw_text(program.screen))
        
    def move_cursor(self,
                    new_cursor_pos: int,
                    ) -> None:
        """
        Move cursor to new position
        :param new_cursor_pos: new cursor position
        """
        self.cursor_pos = new_cursor_pos
        self.cursor_rect.x = self.char_end_pos[self.cursor_pos]
        
    def switch_cursor(self,
                      program,
                      *args, **kwargs) -> bool:
        """
        Switch on/off cursor as a blinking function
        :param program: Program object
        :return: True:go to next event
        """
        if not self.cursor_state:
            self.cursor_state = True
            program.draw_rects.append(self.draw_text(program.screen))
            pg.time.set_timer(
                event=pg.event.Event(CustomUserEvents.CURSOR_SWITCH),
                millis=600,
                loops=1,
            )
            return True
        self.cursor_state = False
        program.draw_rects.append(self.draw_text(program.screen))
        pg.time.set_timer(
            event=pg.event.Event(CustomUserEvents.CURSOR_SWITCH),
            millis=600,
            loops=1,
        )
        return True

    def get_mouse_pos_in_text(self,
                              mouse_x: int,
                              ) -> int:
        """
        Get mouse position in text
        :param mouse_x: mouse x position
        :return: character index
        """
        for i in range(len(self.char_mid_pos) - 2, -1, -1):
            if mouse_x >= self.char_mid_pos[i]:
                return i
        return 0
    
    def highlighting(self,
                     event: pg.event.Event,
                     program,
                     ) -> bool:
        """
        Change highlight area when mousemotion
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event
        """
        char_idx = self.get_mouse_pos_in_text(
            mouse_x=event.pos[0],
        )
        if char_idx != self.highlight_ends[1]:
            self.highlight_ends[1] = char_idx
            program.draw_rects.append(self.draw_text(program.screen))
        return True
    
    def stop_highlighting(self,
                          event: pg.event.Event,
                          program,
                          ) -> bool:
        """
        Stop highlighting process
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        # Check for left mousebutton
        if event.button != pg.BUTTON_LEFT:
            return False
        # Click outside of text area
        if not self.background.rect.collidepoint(event.pos):
            # No highlighted text
            if self.min_highlight() < 0 or self.same_highlight():
                self.highlight_ends[0] = -1
                self.highlight_ends[1] = -1
                self.state = States.STANDARD
                program.draw_rects.append(self.draw_text(program.screen))
                return True
            # Highlighted text
            self.state = States.HIGHLIGHTED
            return True
        # No highlighted text
        if self.min_highlight() < 0 or self.same_highlight():
            self.highlight_ends[0] = -1
            self.highlight_ends[1] = -1
            self.state = States.CURSOR
            self.activate_cursor(
                program=program,
                new_cursor_pos=self.get_mouse_pos_in_text(
                    mouse_x=event.pos[0],
                ),
            )
            return True
        # Highlighted text
        self.state = States.HIGHLIGHTED
        return True
    
    def min_highlight(self) -> int:
        """
        :return: min value in highlight_ends (leftmost position of highlight)
        """
        if self.highlight_ends[0] < self.highlight_ends[1]:
            return self.highlight_ends[0]
        return self.highlight_ends[1]
    
    def max_highlight(self) -> int:
        """
        :return: max value in highlight_ends (rightmost position of highlight)
        """
        if self.highlight_ends[1] > self.highlight_ends[0]:
            return self.highlight_ends[1]
        return self.highlight_ends[0]
    
    def same_highlight(self) -> bool:
        """
        :return: True: if highlight ends are the same; False: not same
        """
        if self.highlight_ends[0] == self.highlight_ends[1]:
            return True
        return False
    
    def textinput(self,
                  event: pg.event.Event,
                  program,
                  ) -> bool:
        """
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        if self.text.rect.width > self.max_text_length:
            return True
        banned = '\\/:*?"<>|'
        if event.text in banned:
            return True
        self.text.change_text(
            new_text=self.text.text[:self.cursor_pos] + event.text + self.text.text[self.cursor_pos:]
        )
        self.update_char_positions()
        if self.cursor_pos < len(self.text.text):
            self.move_cursor(
                new_cursor_pos=self.cursor_pos + 1,
            )
        program.draw_rects.append(self.draw_text(program.screen))
        return True
    
    def keydown(self,
                event: pg.event.Event,
                program,
                ) -> bool:
        """
        Keydown event
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        key_functs = {
            pg.K_BACKSPACE: self.backspace,
            pg.K_DELETE: self.delete,
            pg.K_LEFT: self.step,
            pg.K_RIGHT: self.step,
        }
        try:
            key_functs[event.key](event=event, program=program)
            program.draw_rects.append(self.draw_text(program.screen))
            return True
        except KeyError:
            return False
    
    def backspace(self, *args, **kwargs) -> None:
        """
        Delete backward
        """
        if self.cursor_pos == 0:
            return
        self.text.change_text(
            new_text=self.text.text[:self.cursor_pos - 1] + self.text.text[self.cursor_pos:]
        )
        self.update_char_positions()
        self.move_cursor(
            new_cursor_pos=self.cursor_pos - 1,
        )
        return
    
    def delete(self, *args, **kwargs) -> None:
        """
        Delete forward
        """
        if self.cursor_pos >= len(self.text.text):
            return
        self.text.change_text(
            new_text=self.text.text[:self.cursor_pos] + self.text.text[self.cursor_pos + 1:]
        )
        self.update_char_positions()
        return
    
    def step(self,
             event: pg.event.Event,
             program,
             ) -> None:
        """
        Step cursor with arrow keys left or right in text
        :param event: pygame event
        :param program: Program object
        """
        if event.key == pg.K_LEFT:
            if self.cursor_pos == 0:
                return
            if event.mod & pg.KMOD_SHIFT:
                self.highlight_ends[0] = self.cursor_pos
                self.highlight_ends[1] = self.cursor_pos - 1
                self.deactivate_cursor(program)
                self.state = States.HIGHLIGHTED
                return
            self.move_cursor(new_cursor_pos=self.cursor_pos - 1)
            return
        if self.cursor_pos >= len(self.text.text):
            return
        if event.mod & pg.KMOD_SHIFT:
            self.highlight_ends[0] = self.cursor_pos
            self.highlight_ends[1] = self.cursor_pos + 1
            self.deactivate_cursor(program)
            self.state = States.HIGHLIGHTED
            return
        self.move_cursor(new_cursor_pos=self.cursor_pos + 1)
    
    def highlight_keydown(self,
                          event: pg.event.Event,
                          program,
                          ) -> bool:
        """
        Keydown in highlighted state
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        key_functs = {
            pg.K_BACKSPACE: self.clear_highlight,
            pg.K_DELETE: self.clear_highlight,
            pg.K_LEFT: self.step_out_of_highlight,
            pg.K_RIGHT: self.step_out_of_highlight,
        }
        try:
            key_functs[event.key](program=program, event=event)
            return True
        except KeyError:
            return False
    
    def clear_highlight(self,
                        program,
                        *args, **kwargs) -> None:
        """
        Clear highlight
        :param program: Program object
        """
        self.text.change_text(
            new_text=self.text.text[:self.min_highlight()] + self.text.text[self.max_highlight():]
        )
        self.update_char_positions()
        act_cursor_pos = self.min_highlight()
        self.highlight_ends[0] = -1
        self.highlight_ends[1] = -1
        self.state = States.CURSOR
        self.activate_cursor(
            program=program,
            new_cursor_pos=act_cursor_pos,
        )
        
    def step_out_of_highlight(self,
                              event: pg.event.Event,
                              program,
                              ) -> None:
        """
        Step out of highlight with arrow keys
        :param event: pygame event
        :param program: Program object
        """
        if event.mod & pg.KMOD_SHIFT:
            self.move_highlight(
                event=event,
                program=program,
            )
            return
        if event.key == pg.K_LEFT:
            act_cursor_pos = self.min_highlight()
        else:
            act_cursor_pos = self.max_highlight()
        self.highlight_ends[0] = -1
        self.highlight_ends[1] = -1
        self.state = States.CURSOR
        self.activate_cursor(
            program=program,
            new_cursor_pos=act_cursor_pos,
        )
        
    def move_highlight(self,
                       event: pg.event.Event,
                       program,
                       ) -> None:
        """
        Move highlight with arrow keys
        :param event: pygame event
        :param program: Program object
        """
        if event.key == pg.K_LEFT:
            if self.highlight_ends[1] == 0:
                return
            self.highlight_ends[1] -= 1
            program.draw_rects.append(self.draw_text(program.screen))
            return
        if self.highlight_ends[1] == len(self.text.text):
            return
        self.highlight_ends[1] += 1
        program.draw_rects.append(self.draw_text(program.screen))
        
    def highlight_textinput(self,
                            event: pg.event.Event,
                            program,
                            ) -> bool:
        """
        Textinput into highlight
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        banned = '\\/:*?"<>|'
        if event.text in banned:
            return True
        self.text.change_text(
            new_text=self.text.text[:self.min_highlight()] + event.text + self.text.text[self.max_highlight():]
        )
        self.update_char_positions()
        act_cursor_pos = self.min_highlight() + 1
        self.highlight_ends[0] = -1
        self.highlight_ends[1] = -1
        self.state = States.CURSOR
        self.activate_cursor(
            program=program,
            new_cursor_pos=act_cursor_pos,
        )
        return True

    def update_char_positions(self):
        """
        Update positions in middle of every character and at the beginning and end of string
        """
        self.char_mid_pos.clear()
        self.char_mid_pos.append(self.text.rect.left)
        prev_right = self.char_mid_pos[-1]
        self.char_end_pos.clear()
        self.char_end_pos.append(self.text.rect.left)
        for i in range(1, len(self.text.text) + 1):
            short_text = Text(
                text=self.text.text[:i],
                text_type=self.text.type,
                size=self.text.size,
                color="black",
                anchor_type='midleft',
                anchor_pos=self.text.rect.midleft,
            )
            self.char_mid_pos.append(
                prev_right + ((short_text.rect.right - prev_right) // 2)
            )
            prev_right = short_text.rect.right
            self.char_end_pos.append(short_text.rect.right)
        self.char_mid_pos.append(self.text.rect.right)
        
    def draw_text(self,
                  surf: pg.Surface,
                  ) -> pg.Rect:
        """
        Draw text area of textbox on surface
        :param surf: surface
        :return: rectangle area for draw_rect list
        """
        self.background.draw(surf)
        if self.min_highlight() >= 0:
            pg.draw.rect(
                surface=surf,
                color=self.highlight_color,
                rect=pg.Rect(
                    self.char_end_pos[self.min_highlight()],
                    self.highlight_top,
                    self.char_end_pos[self.max_highlight()] - self.char_end_pos[self.min_highlight()],
                    self.highlight_height
                ),
            )
        self.text.draw(surf)
        if self.cursor_state:
            pg.draw.rect(
                surface=surf,
                color=C.BLACK,
                rect=self.cursor_rect,
            )
        return self.background.rect
    
    def draw(self,
             surf: pg.Surface,
             ) -> pg.Rect:
        """
        Draw textbox object
        :param surf: surface
        :return: rectangle area for draw_rect list
        """
        self.frame.draw(surf)
        self.draw_text(surf)
        return self.rect
    
    def update_text(self,
                    new_text: str,
                    surf: pg.Surface,
                    ) -> pg.Rect:
        """
        Change text and redraw
        :param new_text: new text
        :param surf: surface
        :return rect area to draw
        """
        self.text.change_text(new_text=new_text)
        self.update_char_positions()
        self.background.draw(surf)
        self.text.draw(surf)
        return self.background.rect
    
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
        self.background.reposition(x_diff, y_diff)
        self.frame.reposition(x_diff, y_diff)
        self.text.reposition(x_diff, y_diff)
        self.cursor_rect.x += x_diff
        self.cursor_rect.y += y_diff
        
        
class FileWinTextBox(TextBox):
    """
    TextBox for file window
    """

    def __init__(self,
                 rect: pg.Rect,
                 frame_thickness: int,
                 frame_top_color: tuple,
                 frame_bottom_color: tuple,
                 frame_edge_lines: tuple,
                 text_size: int,
                 text_type: str,
                 align: str,
                 start_text: str = None,
                 ) -> None:
        """
        Initialize file window TextBox object
        :param rect: rectangle area of object
        :param frame_thickness: frame thickness
        :param frame_top_color: frame top&left color
        :param frame_bottom_color: frame bottom&right volor
        :param frame_edge_lines: frame edge line codes
        :param start_text: starting text
        :param text_size: size of text
        :param text_type: path to text type (.ttf)
        :param align: "left" or "right" alignment
        """
        super().__init__(
            rect=rect,
            frame_thickness=frame_thickness,
            frame_top_color=frame_top_color,
            frame_bottom_color=frame_bottom_color,
            frame_edge_lines=frame_edge_lines,
            text_size=text_size,
            text_type=text_type,
            align=align,
            start_text=start_text
        )
        
    def event_manager(self,
                      event: pg.event.Event,
                      program,
                      file_win,
                      ) -> bool:
        """
        Event manager for textbox
        :param event: pygame Event
        :param program: Program object
        :param file_win: FileWindow object
        :return: True: go to next event; False: go to next event manager
        """
        old_text = self.text.text
        event_result = self.event_managers[self.state].handle(
            event=event,
            program=program,
        )
        if old_text != self.text.text:
            self.check_file_list(
                program=program,
                file_win=file_win,
            )
        return event_result
    
    def keydown(self,
                event: pg.event.Event,
                program,
                ) -> bool:
        """
        Keydown event
        :param event: pygame event
        :param program: Program object
        :return: True:go to next event; False:go to next event manager
        """
        key_functs = {
            pg.K_BACKSPACE: self.backspace,
            pg.K_DELETE: self.delete,
            pg.K_LEFT: self.step,
            pg.K_RIGHT: self.step,
            pg.K_UP: self.no,
            pg.K_DOWN: self.no,
        }
        try:
            key_functs[event.key](event=event, program=program)
            program.draw_rects.append(self.draw_text(program.screen))
            return True
        except KeyError:
            return False
        
    def no(self, *args, **kwargs):
        return

    def check_file_list(self,
                        program,
                        file_win,
                        ) -> None:
        """
        Check file list if textbox text is in file names list
        :param program: Program object
        :param file_win: FileWindow object
        """
        found_idx = file_win.list.find_name(name=self.text.text)
        if found_idx == file_win.list.clicked_idx:
            return
        if found_idx < 0:
            if file_win.list.clicked_idx >= 0:
                program.draw_rects.append(file_win.list.update_list(
                    surf=program.screen,
                    new_clicked_idx=found_idx,
                ))
        else:
            program.draw_rects.append(file_win.list.update_list(
                surf=program.screen,
                new_clicked_idx=found_idx,
            ))
    
    def change_text_highlight_all(self,
                                  new_text: str,
                                  program,
                                  ) -> None:
        """
        Change text and highlight all text
        :param new_text: new text
        :param program: Program object
        """
        self.text.change_text(new_text=new_text)
        self.update_text(
            new_text=new_text,
            surf=program.screen,
        )
        self.state = States.HIGHLIGHTED
        self.highlight_ends[0] = 0
        self.highlight_ends[1] = len(self.text.text)
        self.deactivate_cursor(program)
        
    def unhighlight(self,
                    program,
                    ) -> None:
        """
        Remove highlight
        :param program: Program object
        """
        self.state = States.STANDARD
        self.highlight_ends[0] = -1
        self.highlight_ends[1] = -1
        program.draw_rects.append(self.draw_text(program.screen))
    