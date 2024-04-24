import pygame as pg


def standard_mousebuttondown(
        event: pg.event.Event,
        program,
) -> bool:
    """
    Mousebuttondown event handler in standard state
    :param event: pygame event
    :param program: Program object
    :return: True: go to next event; False: go to next event handler
    """
    print('mousebuttondown')
    return False


def standard_mousebuttonup(
        event: pg.event.Event,
        program,
) -> bool:
    """
    Mousebuttonup event handler in standard state
    :param event: pygame event
    :param program: Program object
    :return: True: go to next event; False: go to next event handler
    """
    print('mousebuttonup')
    return False


def standard_mousemotion(
        event: pg.event.Event,
        program,
) -> bool:
    """
    Mousemotion event handler in standard state
    :param event: pygame event
    :param program: Program object
    :return: True: go to next event; False: go to next event handler
    """
    print('mousemotion')
    return False
