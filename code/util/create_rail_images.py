import pygame as pg

pg.init()
pg.display.set_mode((10, 10))


def create_img(rail_type: str):
    img = pg.image.load(
        f"C:/Users/M/PycharmProjects/rail_scheduler_v2/resources/graphics/creation/rail_{rail_type}.BMP").convert()
    size = img.get_size()
    new_img = pg.Surface(size)
    new_img.fill("black")
    new_img.set_colorkey("black")
    for y in range(size[1]):
        for x in range(size[0]):
            px = img.get_at((x, y))
            if px[:3] == (0, 0, 0):
                new_img.set_at((x, y), "white")
    pg.image.save(
        new_img,
        f"C:/Users/M/PycharmProjects/rail_scheduler_v2/resources/graphics/rail_{rail_type}.BMP"
    )
    
    
rail_types = ("straight", "diag", "turn", "diagturn", "bend", "diagbend", "diag_corner")
for i in range(len(rail_types)):
    create_img(rail_types[i])
    