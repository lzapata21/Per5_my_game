 this file was created by: Chris Cozort
# github test
# this is where we import libraries and modules
import pygame as pg
from settings import *
from utils import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
# we are editing this file after installing git
# git test

'''
Elevator pitch: I want to create a game that follows an apprentice mage from the bottom of a tower to the top, leveling up as he climbs to the top to defeat the evil wizard...

GOALS: to ascend the tower
RULES: jump, cast spells, shields attack, cannot move up until puzzles and enemies defeated 
FEEDBACK: Damage meter, spells interactions 
FREEDOM: x and y movement with jump, platforming

What's the sentence: Shoot iceblock with fireball melt iceblock to advance...

Alpha goal: to create a sidescroller setup gravity, platform collision, jump

'''

'''
Sources:
https://www.pygame.org/docs/ref/mouse.html - used to see if mouse is clicked

'''

# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chris' Coolest Game Ever...")
    self.playing = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'dk_level1.txt'))
  def load_level(self, level):
    # kill all sprites to free up memory
    for s in self.all_sprites:
       s.kill()
       print(len(self.all_sprites))
    # From load data to create new map object with level parameter
    self.map = Map(path.join(self.game_folder, level))

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
        # if tile == 'B':
        #   Barrel(self, col, row)
  def new(self):
    self.load_data()

    # create game countdown timer
    self.game_timer = Timer(self)
    # set countdown amount
    self.game_timer.cd = 45

    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_platforms = pg.sprite.Group()
    self.all_portals = pg.sprite.Group()
    self.all_barrels = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    self.all_projectiles = pg.sprite.Group()
    # instantiating the class to create the player object 
    # self.player = Player(self, 5, 5)
    # self.mob = Mob(self, 100, 100)
    # self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # # instantiates wall and mob objects
    # for i in range(12):
    #   Wall(self, TILESIZE*i, HEIGHT/2)
    #   Mob(self, TILESIZE*i, TILESIZE*i)
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
        if tile == 'T':
          Portal(self, col, row)
        # if tile == 'L':
        #   Moving_Platform(self, col, row)
        # if tile == 'B':
        #   Barrel(self, col, row)
         

# this is a method
# methods are like functions that are part of a class
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
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):

    self.game_timer.ticking()
    # if self.game_timer.cd < 40:
    #   for s in self.all_sprites:
    #     s.kill()
    #   self.load_level("level2.txt")
    # update all the sprites...and I MEAN ALL OF THEM
    # for w in self.all_walls:
    #   if self.player.pos.x > WIDTH - WIDTH/3:
    #     w.rect.x -= self.player.vel.x
    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  # output
  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  g.run()
  