import pygame as pg
from settings import *
vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []

        self.read(filename)
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
    
    def read(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            lines = f.read().splitlines()
            for line in lines:
                self.data.append(line)

    def write(self, filename, _list):
        with open(filename, 'w') as f:
            for line in _list:
                f.write(line + '\n')
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

        self.shaking = False
        self.shake_offset = vec(0, 0)
        self.last_shake = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def shake(self):
        self.shaking = True

    def update(self, target):
        self.x = -target.rect.x + int(WIDTH / 2)
        self.y = -target.rect.y + int(HEIGHT / 2)

        if self.shaking:
            if self.last_shake == 0:
                self.last_shake = 1
                self.shake_offset += vec(2, 2)
            else:
                self.last_shake = 0
                self.shake_offset -= vec(2, 2)

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom
        self.camera = pg.Rect(self.x - self.shake_offset.x, self.y - self.shake_offset.y, self.width, self.height)
