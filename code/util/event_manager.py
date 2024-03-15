import pygame as pg


class EventManager:
    """
    Event manager for pygame events
    Event handler functions receive following parameters:
     event (pygame.event.Event), program (Program)
    """
    def __init__(self,
                 event_types: tuple or list,
                 event_functions: tuple or list,
                 ) -> None:
        """
        Initialize event manager
        :param event_types: list of pygame event type codes
        :param event_functions: list of event handler functions in identical order
        """
        if len(event_functions) != len(event_types):
            raise ValueError("Not identical amount of elements in event_types and event_functions")
        
        self.event_handlers = dict()
        for i in range(len(event_types)):
            self.event_handlers[event_types[i]] = event_functions[i]

    def handle(self,
               event: pg.event.Event,
               program=None,
               ) -> bool:
        """
        Handle event
        :param event: pygame event
        :param program: Program object
        :return: bool True:go to next event; False:go to next event manager
        """
        try:
            return self.event_handlers[event.type](
                event=event,
                program=program)
        except KeyError:
            return False
        