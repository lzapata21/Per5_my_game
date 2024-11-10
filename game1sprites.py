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
        Sprite. __init__(self, self.groups)
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
        self.cd = Cooldown()
        self.invulnerable = Cooldown()
        self.jumping = False
        self.health = 100
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()

# this is damage when in lava
    def shoot(self):
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.cd.delta > .01:
            print("taking damage")
           
    def jump(self):
        print("im trying to jump")
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
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
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
        #         print("Collided on x axis")
        #     else:
        #         print("not working...for hits")
        # else:
        #     print("not working for dir check")
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            # if str(hits[0].__class__.__name__) == "Powerup":
            #     print("i collide with powerup")
            #     for m in self.game.all_mobs:
            #         print("trying to increase mob speed")
            #         m.speed = 20
            #         print(m.speed)
            #     print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1
            if str(hits[0].__class__.__name__) == "Portal":
                self.game.load_level("level2.txt")
                # in class figure out how to make another level
            if str(hits[0].__class__.__name__) == "Lava":
                self.invulnerable.event_time = floor(pg.time.get_ticks()/1000)
                if self.invulnerable.delta > .01:
                    self.health -= 1
            if str(hits[0].__class__.__name__) == "Mob":
                if self.vel.y > 0:
                    print("collided with mob")
                    hits[0].kill()
                else:
                    print("ouch I was hurt!!!")

    def update(self):
        self.cd.ticking()
        self.invulnerable.ticking()           
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
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
        pass
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        if self.rect.colliderect(self.game.player):
            self.speed *= -1


    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH-64 or self.rect.x < 64:
            self.speed *= -1
            self.rect.y += 64

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

class Portal(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_portals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Lava(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_lava
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE