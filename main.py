import pygame as pg
import os
from collections import deque
from settings import *

vec = pg.math.Vector2
arrows = {}

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

folder = os.path.dirname(__file__)
home_img = pg.image.load(os.path.join(folder, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (40, 40))
start_img = pg.image.load(os.path.join(folder, 'target.png')).convert_alpha()
start_img = pg.transform.scale(start_img, (40, 40))
arrow_img = pg.image.load(os.path.join(folder, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (40, 40))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), 
            (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1), 
                            vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neightbors = [node + connection for connection in self.connections]
        # if (node.x + node.y) % 2:    # for 4 directions
        #     neightbors.reverse()
        neightbors = filter(self.in_bounds, neightbors)
        neightbors = filter(self.passable, neightbors)
        # print(list(neightbors))
        return neightbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGREY, rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

def vec2int(v):
    return (int(v.x), int(v.y))

def draw_icons():
    goal_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    goal_rec = home_img.get_rect(center=goal_center)
    screen.blit(home_img, goal_rec)

    start_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    start_rec = start_img.get_rect(center=start_center)
    screen.blit(start_img, start_rec)




def breadth_first_search(graph, goal, start):
    frontier = deque()
    frontier.append(goal)
    path = {}   # key:tile, value:direction we came from
    path[vec2int(goal)] = None
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == start:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)] = current - next
    return path


g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)

# walls = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (1, 6), (3, 6), (0, 11), (1, 11), (2, 11), (5, 3), (6, 3), (7, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 7), (7, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (6, 12), (7, 12), (8, 3), (9, 3), (9, 2), (9, 1), (10, 3), (11, 3), (14, 1), (14, 0), (10, 7), (11, 7),
#          (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (11, 12), (10, 12), (13, 7), (14, 7), (15, 7), (14, 6), (16, 7), (17, 7), (18, 7), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (18, 10), (19, 10), (20, 10), (20, 11), (20, 12), (23, 14), (23, 13), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10), (21, 7), (21, 6), (21, 5), (22, 5), (23, 5), (24, 5), (25, 5), (21, 4), (21, 3), (21, 2), (17, 3)]
# for wall in walls:
#     g.walls.append(vec(wall))

goal = vec(14, 8)
start = vec(20, 0)
path = breadth_first_search(g, goal, start)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                print([(int(loc.x), int(loc.y)) for loc in g.walls])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            # draw walls
            if event.button == 1:
                if mpos != goal and mpos != start:
                    if mpos in g.walls:
                        g.walls.remove(mpos)
                    else:
                        g.walls.append(mpos)
            # select target
            if event.button == 2:
                if mpos not in g.walls:
                    start = mpos
            # select home
            if event.button == 3:
                if mpos not in g.walls:
                    goal = mpos
            path = breadth_first_search(g, goal, start)

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGREY)
    # fill explored area
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDGRAY, rect)
    draw_grid()
    g.draw()
    # drawing icons
    draw_icons()
    # draw path from start to goal
    current = start + path[vec2int(start)]
    while current != goal:
        x = current.x * TILESIZE + TILESIZE / 2
        y = current.y * TILESIZE + TILESIZE / 2
        img = arrows[vec2int(path[vec2int(current)])]
        rec = img.get_rect(center=(x, y))
        screen.blit(img, rec)
        # find next node in path
        current = current + path[vec2int(current)]

    pg.display.flip()
