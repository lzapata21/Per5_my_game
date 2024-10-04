
# omprt 
import pygame as pg
from settings import *
from sprites import *



class Game: 
  def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("My Game")
      self.playing = True
      # this sets up the first part of the game setting time, height and width 
  def new(self):
      # create a sprite group using the pg library
      self.all_sprites = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
    #  instantiating the class to create the player object 
      self.player = Player(self, 5, 5)
      self.mob = Mob(self, 100, 100)
      self.wall = Wall(self, WIDTH/2, HEIGHT/2)
      # this sets the dimensions of the objects in game
#adding player to all the sprites group
      for i in range(6):
        w = Wall(self, TILESIZE*i, TILESIZE*i)
        print(w.rect.x)
        m = Mob(self, TILESIZE*i, TILESIZE*i)
    #  size of object which is being imported from settings
      
# this is a method
# methods are functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()
      
      pg.quit()
    #  input
  def events(self):
      for event in pg.event.get():
          if event.type == pg.QUIT:
            self.playing = False
# this is a method
# methods are functions that are part of a class
# the run method runs the game loop
  def update(self):
      # update all the sprites
      self.all_sprites.update()
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running")
  pg.init()
  g = Game()
  print("main is running")
  g.new()
  g.run()