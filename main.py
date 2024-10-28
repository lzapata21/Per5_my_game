# gittest
# omprt 
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import * 
from tilemap import *
from os import path
'''


GOALS: 
FREEDOMS:
FEEDBACK:
RULES:
what's the sentence: player 1 collides with enemy and enemy bounces off...

'''

class Game: 
  def __init__(self):
    pg.init()
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("My Game")
    self.playing = True
      # this sets up the first part of the game setting time, height and width 

  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'level1.txt'))
  def new(self): 
    self.load_data()
    print(self.map.data)
    # create a sprite group using the pg library
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    #  instantiating the class to create the player object 
  #     self.player = Player(self, 5, 5)
  #     self.mob = Mob(self, 100, 100)
  #     self.wall = Wall(self, WIDTH/2, HEIGHT/2)
  #       # this sets the dimensions of the objects in game
  # #adding player to all the sprites group
  #     for i in range(6):
  #         w = Wall(self, TILESIZE*i, TILESIZE*i)
  #         print(w.rect.x)
  #         m = Mob(self, TILESIZE*i, TILESIZE*i)
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
    

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
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, 'JUMP', 24, WHITE, WIDTH/2, HEIGHT/2 )
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running")
  pg.init()
  g = Game()
  print("main is running")
  g.new()
  g.run()