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
    self.currentLevel = 2
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
      #  print(len(self.all_sprites))
    # From load data to create new map object with level parameter
    self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))
    # kill all sprites to free up memory
    # self.currentLevel += 1
    # self.all_sprites.empty()
    # self.all_walls.empty()
    # self.all_lava.empty()
    # self.all_mobs.empty()
    # self.all_portals.empty()
    
      #  print(len(self.all_sprites))
    # From load data to create new map object with level parameter
    # self.map = Map(path.join(self.game_folder, "level" + str(self.currentLevel) + ".txt"))

         


  
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

    # if self.player.health <=0:
    #   self.show_end_screen()
    #   return
   
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
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.current_time), 24, BLACK, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, str(self.score), 24, BLACK, WIDTH-100, 50)
    self.draw_text(self.screen, "Best score " + str(self.highscore), 24, BLACK, WIDTH-100, 100)
    pg.display.flip()

  def show_start_screen(self):
        self.load_data()
        if not self.running:
            return
        if path.exists(HS_FILE):
          # print("this exists...")
          with open(path.join(self.game_folder, HS_FILE), 'r') as f:
            self.best_time = int(f.read())
        else:
          with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                  f.write(str(0))
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "you are in the matrix", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Best score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press di buton agyen bomboclat", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
  
  def show_end_screen(self):
        # print("File created and written successfully.")
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "You're done! ", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "count ya coins: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

  
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
  # instantiate
  g = Game()
  g.show_start_screen()
  while g.playing:
    g.new()
    g.run()
  g.show_end_screen()
  
