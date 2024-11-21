import pygame as pg
from game1sprites import *
from game1settings import *
from os import path 
from game1tilemap import *
from utils import *


'''

GOALS: make game work/run without errors, reach the top of the platform, make mobs, make walls, make clock, one game has bones/starts to run-add power ups(limited by time)
FREEDOMS: can jump but has walls on each side to stay in map, movement is up, down, left, right, and second level is floor is lava
FEEDBACK: when jumping/moving there is gravity + friction 
RULES: no powerups, but there is mobs and walls that cannot be passed, make it all the way to the top without falling, fastest to the top wins 

'''


def draw_stat_bar(surf, x, y, w, h, pct, fill_color, outline_color):
    if pct < 0:
        pct = 0
    BAR_LENGTH = w
    BAR_HEIGHT = h
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, fill_color, fill_rect)
    pg.draw.rect(surf, outline_color, outline_rect, 2)

class Game:
  def __init__(self):
    pg.init()
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("jump master")
    self.playing = True
    self.running = True
    self.score = 0
    self.highscore = 0
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'game1level2.txt'))
  def load_level(self, level):

    # kill all sprites to free up memory
    for s in self.all_sprites:
        s.kill()
    self.map = Map(path.join(self.game_folder, level))
      #  print(len(self.all_sprites))

  def new(self):
    self.load_data()
    self.game_timer = Timer(self)
    self.game_timer.cd = 45

    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_lava = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group() 
    # self.all_portals = pg.sprite.Group()
# import map but rewrite when comes the time
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        # print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        
        if tile == 'C':
          Coin(self, col, row)
        # if tile == '0':
        #   Portal(self, col, row)
       
        if tile == 'L':
          Lava(self, col, row)
        
          
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
         


    

  
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
          if self.playing:
            self.playing = False
          self.running = False

  def update(self):
    self.game_timer.ticking()
    self.player.health -= 1
    hits  = pg.sprite.spritecollide(self.player, self.all_mobs, False)
    if hits:
       print("i hit something...")
    

    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  def draw(self):
    self.screen.fill(WHITE)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.player.health), 24, BLACK, WIDTH/2, HEIGHT/2)
    print(self.player.health)
    draw_stat_bar(self.screen, 5, 5, 150, 25, self.player.health, RED, WHITE)
    # self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    # self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/16)
    # self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    # self.draw_text(self.screen, 'JUMP', 24, WHITE, WIDTH/2, HEIGHT/2)
    pg.display.flip()
    # note:check color and position for health
  

  def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


if __name__ == "__main__":
  pg.init()
  g = Game()
  while g.playing:
    g.new()
    g.run()