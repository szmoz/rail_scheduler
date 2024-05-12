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
    
# Set rail pixel lines
from code.camera.variable_data import RAIL_PIXELS as rp

# 90
new_coord = []
for px in rp[7]:
    new_coord.append((px[0], 10 + (10 - px[1])))
    
rotated_new_coord = []
for px in new_coord:
    rotated_new_coord.append([px[1] * -1, px[0]])

for px in rotated_new_coord:
    px[0] += 20

for px in rotated_new_coord:
    print(f"        ({px[0]}, {10 + (10 - px[1])}),")

# 180
new_coord = []
for px in rp[2]:
    new_coord.append((px[0], 10 + (10 - px[1])))

rotated_new_coord = []
for px in new_coord:
    rotated_new_coord.append([px[0] * -1, px[1] * -1])

for px in rotated_new_coord:
    px[0] += 20
    px[1] += 20

for px in rotated_new_coord:
    print(f"        ({px[0]}, {10 + (10 - px[1])}),")

# 270
new_coord = []
for px in rp[2]:
    new_coord.append((px[0], 10 + (10 - px[1])))
    
rotated_new_coord = []
for px in new_coord:
    rotated_new_coord.append([px[1], px[0] * -1])
    
for px in rotated_new_coord:
    px[1] += 20
    
for px in rotated_new_coord:
    print(f"        ({px[0]}, {10 + (10 - px[1])}),")

    
print("")
# reverse
new_rp = []
for px in rp[2]:
    new_rp.append(px)
new_rp = new_rp.__reversed__()
for px in new_rp:
    print(f"        ({px[0]}, {px[1]}),")

