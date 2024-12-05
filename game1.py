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
# this is where the health bar is showing color and position

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
    self.currentLevel = 1
    # load map
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
    #    f.write(str(0))
    try:
      with open(path.join(self.game_folder, HS_FILE), 'r') as f:
          self.highscore = int(f.read())
    except:
       self.highscore = 0
       with open(path.join(self.game_folder, HS_FILE), 'w') as f:
          f.write(str(self.highscore))
        



    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
  def load_next_level(self):
    # kill all sprites to free up memory
    self.currentLevel += 1
    for s in self.all_sprites:
       s.kill()
       print(len(self.all_sprites))
    # # From load data to create new map object with level parameter
    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + "txt"))

  def new(self):
    self.load_data()
    self.game_timer = Timer(self)
    self.game_timer.cd = 45
# where the game sprites know what is in the game
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_lava = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group() 
    self.all_portals = pg.sprite.Group()
    # self.all_portals = pg.sprite.Group()
# classification for tilemap(s)
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
        if tile == 'L':
          Lava(self, col, row)
        if tile == '0':
           Portal(self, col, row)
          
    for row, tiles in enumerate(self.map.data):
      # print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        if tile == 'P':
          self.player = Player(self, col, row)
         


    
# this runs the game and is where game updates
  
  def run(self):
    self.running = True
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      self.events()
      self.update()
      self.draw()
    pg.quit()
    

  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          if self.score > self.highscore:
             with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(self.score))   
          self.running = False
          self.playing = False

  def update(self):
    self.game_timer.ticking()
   
    hits  = pg.sprite.spritecollide(self.player, self.all_mobs, False)
    if hits:
       print("i hit something...")
    
# drawing map
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
    draw_stat_bar(self.screen, 5, 5, 150, 25, self.player.health, RED, WHITE)
    self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, BLACK, WIDTH / 2, HEIGHT / 12)
    self.draw_text(self.screen, "Current Score: " + str(self.score), 24, BLACK, WIDTH / 2, HEIGHT / 22)
    # self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)d
    # self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    # self.draw_text(self.screen, 'JUMP', 24, WHITE, WIDTH/2, HEIGHT/2)
    pg.display.flip()
    
  

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