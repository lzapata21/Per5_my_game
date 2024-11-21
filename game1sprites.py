import pygame as pg
from pygame.sprite import Sprite
from game1settings import *
from random import randint
from utils import *
# notes to fix for screen size, player spawnpoint, and mob spawn points:


vec = pg.math.Vector2
class Player(Sprite):
         
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 3
        self.coin_count = 0
        self.jump_power = 15
        self.jumping = False
        self.cd = Cooldown()
        self.invulnerable = Cooldown()       
        self.health = 100
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.shoot()
        if keys[pg.K_w]:
            self.vel.y -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_s]:
            self.vel.y += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()

            

           
    def jump(self):
        # print("im trying to jump")
        print(self.vel.y)
        self.rect.y += 2
        whits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        phits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if whits or phits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print('still trying to jump...')
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            pass
            # if str(hits[0].__class__.__name__) == "Coin":
            #     print("I got a coin!!!")
            #     self.coin_count += 1
            # if str(hits[0].__class__.__name__) == "Lava":
            #     self.health -= 1
                # print(self.health)
        


    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')
    
        # teleport the player to the other side of the screen
        # self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_lava, False)
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
        
        
       
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        if self.rect.colliderect(self.game.player):
            self.speed *= -1    

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# class Portal(Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.all_portals
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

class Lava(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_lava
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE