from pygame import *
from random import randint
from time import time as timer

mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()

#fire_sound = mixer.Sound('fire.ogg')
#fire_sound.play()

font.init()
font1 = font.Font(None, 50)
font2 = font.Font(None, 30)
lose = font1.render("You Lose", True, (180, 0, 0))
win = font1.render("You Win", True, (180, 0, 0))

img_back = "galaxy.jpg" 
img_hero = "rocket.png"  
img_bullet = "bullet.png" 
img_enemy = "ufo.png"   
 
score = 0  
lost = 0
num_fire = 0
rel_time = False
goal = 10000
max_lost = 3 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 50:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 25, 15, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
  
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
if rel_time:
    now_time = timer()
    if now_time - last_time < 3:
        pass
    else:
        num_fire =0
        rel_timer = False

finish = False
run = True 
scaling = 10
a = 0
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #if num_fire < 15 and rel_time == False:
                #    num_fire +=1
                    ship.fire()
                #if num_fire < 15 and rel_time == False:
                #    last_timer = timer()
                #    rel_time == True
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score += 1
            if a >= 10:
                scaling += 1
                print(scaling)
                a = 0
            else:
                a += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit((lose), (200, 200))
        if score >= goal:
            finish = True
            window.blit((win), (200, 200))



    clock.tick(scaling)
    display.update()