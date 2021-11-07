from pygame import *
from random import randint
from time import time as timer
win_width = 700
x = 50
score = 0
goal = 20
lost = 0
max_lost = 10
life =3 
img_bullet = ("bullet.png")
img_bullet1 = ("bullet2.png")
img_bullet2 = ("bullet1.png")
img_enemy = ("ufo.png")
img_ast  = "asteroid.png"
#a = randint(10,650)
#b = randint(10,650)
#c = randint(10,650)
#d = randint(10,650)
#e = randint(10,650)
#f = randint(10,650)
lost =0
y = 50
win_heihgt = 500
window = display.set_mode((win_width,win_heihgt))
display.set_caption("Шутер")
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, ( self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -=5
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x +=5
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.x,self.rect.y-55,-15)
        bullets.add(bullet)
    def fire1(self):
        bullet = SuperBullet(img_bullet1,self.rect.x,self.rect.y-55,-15)
        bullets.add(bullet)
    def fire2(self):
        bullet = SuperBullet1(img_bullet2,self.rect.x,self.rect.y-55,-15)
        bullets.add(bullet)
class SuperBullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed
        if self.rect.y < 0:
            self.kill()
class SuperBullet1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x -= self.speed
        if self.rect.y < 0:
            self.kill()


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



class Enemy(GameSprite):
    direction = "down"
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_heihgt:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1
        
font.init()
font1 = font.Font(None,36)
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40,randint(1,2))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80, win_width - 80),-40,randint(1,3))
    monsters.add(monster)

num_fire = 0
rel_time = False

finish = False
   

player = Player("rocket.png", 5, win_heihgt - 80,4)
#ufo = Enemy("ufo.png",a,0,1)
#ufo1 = Enemy("ufo.png",b,0,1)
#ufo2 = Enemy("ufo.png",c,0,1)
#ufo3 = Enemy("ufo.png",d,0,1)
#ufo4 = Enemy("ufo.png",e,0,1)
#ufo5 = Enemy("ufo.png",f,0,1)
background = transform.scale(image.load("galaxy.jpg"),(700,500))

clock = time.Clock()
FPS=60

mixer.init()
mixer.music.load('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()
x = 50
y = 50
now_time = timer()
x1 = 100
keys_pressed = key.get_pressed()
firing = mixer.Sound("fire.ogg")
collides = sprite.groupcollide(monsters,bullets,True,True)
y2 = 100
game = True
shoot = False
shoot1 = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            shoot = True
        if e.type == KEYUP:
            shoot = False
    if shoot:
        player.fire()
        firing.play()
    if shoot1:
        player.fire1()
        firing.play()
        player.fire2()
        firing.play()
    if not finish:

        player.update()
        #ufo.update()
        #ufo1.update()
        #ufo2.update()
        #ufo3.update()
        #ufo4.update()
        text_lose = font1.render("Пропущено:" + str(lost),1,(100,150,90))
        #text_win = font1.render("Убито:" + score,1,(255,150,90))
        lose = font1.render("YOU LOSE",1,(255,255,255))
        #ufo5.update()
        window.blit(background,(0,0))
        window.blit(text_lose,(50,50))
        #window.blit(text_win,(50,100))
        player.reset()
        #ufo.reset()
        #ufo1.reset()
        #ufo2.reset()
        #ufo3.reset()
        #ufo4.reset()
        #ufo5.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        
        for c in collides:
            monster = Enemy(img_enemy,randint(80, win_width - 80),-40,randint(1,3))
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or lost >= 3:
            finish = True
            window.blit(lose,(350,200))
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))    
        if score >= 10:
            finish = True
            window.blit(win,(200,200))     
        display.update()
        clock.tick(FPS)        
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
    


