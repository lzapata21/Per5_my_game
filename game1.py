import pygame as pg
from game1sprites import *
from game1settings import *
from os import path 
from game1tilemap import *


'''

GOALS: make game work/run without errors, reach the top of the platform, make mobs, make walls, make clock
FREEDOMS: can jump but has walls on each side to stay in map, movement is up, down, left, right,
FEEDBACK: when jumping/moving there is gravity + friction 
RULES: no powerups, but there is mobs and walls that cannot be passed, make it all the way to the top without falling, fastest to the top wins 

'''

class Game:
    def __init__(self):
      pg.init()
      pg.mixer.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("jump master")
      self.playing = True

# import map but rewrite when comes the time

    def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.map = Map(path.join(self.game_folder, 'level2.txt'))
    def new(self):
      self.load_data()
      print(self.map.data)

      self.all_sprites = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()

      for row, tiles in enumerate(self.map.data):
        print(row*TILESIZE)
        for col, tile in enumerate(tiles):
          print(col*TILESIZE)
          if tile == '1':
            Wall(self, col, row)
          if tile == 'M':
            Mob(self, col, row)