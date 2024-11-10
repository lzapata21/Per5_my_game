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

class Game:
  def __init__(self):
    pg.init()
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("jump master")
    self.playing = True
  def load_level(self, level):
    # kill all sprites to free up memory
    for s in self.all_sprites:
       s.kill()
      #  print(len(self.all_sprites))
    self.map = Map(path.join(self.game_folder, level))

# import map but rewrite when comes the time
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'game1level2.txt'))

  def new(self):
    self.load_data()
    self.game_timer = Timer(self)
    self.game_timer.cd = 45

    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_lava = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_mobs = pg.sprite.Group()
    self.all_portals = pg.sprite.Group()


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
        if tile == 'C':
          Coin(self, col, row)
        if tile == '0':
          Portal(self, col, row)
        if tile == 'L':
          Lava(self, col, row)

                   
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
    if self.player.health < 95:
      self.playing = False
    #   if self.game_timer.cd < 40:
    #     for s in self.all_sprites:
    #       s.kill()
    # self.load_level("game1lvl2.txt")
    

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
    self.draw_text(self.screen, str(self.player.health), 24, BLACK, WIDTH/2, HEIGHT/2)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.get_countdown()), 24, WHITE, WIDTH/30, HEIGHT/16)
    self.draw_text(self.screen, 'JUMP', 24, WHITE, WIDTH/2, HEIGHT/2)
    pg.display.flip()
  
  def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(WHITE)
        self.draw_text(self.screen, "GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(self.screen, "NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        else:
            self.draw_text(self.screen, "High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
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
  print("Main works")
  pg.init()
  g = Game()
  print("main works")
  g.new()
  g.run()