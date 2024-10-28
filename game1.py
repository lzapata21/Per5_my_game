import pygame as pg
from game1sprites import *
from game1settings import *
from os import path 
from game1tilemap import *


'''

GOALS: make game work/run without errors, reach the top of the platform, make mobs, make walls, make clock, one game has bones/starts to run-add power ups(limited by time)
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
    self.map = Map(path.join(self.game_folder, 'game1level2.txt'))
  def new(self):
    self.load_data()
    print(self.map.data)

    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
      

    # self.player = Player(self, 5, 5)
    # self.mob = Mob(self, 100, 100)
    # self.wall = Wall(self, WIDTH/2, HEIGHT/2)


    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      self.events()
      self.update()
      self.draw()
    pg.quit()

  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  def update(self):
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
    self.draw_text(self.screen, 'JUMP', 24, WHITE, WIDTH/2, HEIGHT/2)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    pg.display.flip()

if __name__ == "__main__":
  print("Main works")
  pg.init()
  g = Game()
  print("main works")
  g.new()
  g.run()