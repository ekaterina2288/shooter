from pygame import *
from random import randint
font.init()
mixer.init()

lost = 0
lost_max = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def strike(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(5, 630)
            self.rect.y = -50
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption('Шутер')
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'), (win_w, win_h))
player = Player('rocket.png', 330, 430, 60, 70, 5)
monsters = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', randint(5, 630), -50, 70, 50, randint(1,2))
    monsters.add(monster)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font = font.Font(None, 70)
win = font.render('You win!', True, (206,209,0))
lose = font.render('You lose!', True, (180,3,0))

game = True
finish = False

score = 0
while game:
    window.blit(background, (0,0))
    player.reset()
    monsters.draw(window)
    bullets.draw(window)
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key ==  K_SPACE:
                player.strike()
                fire_sound.play()
    
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides: 
        score += 1
        monster = Enemy('ufo.png', randint(5, 630), -50, 70, 50, randint(1,2))
        monsters.add(monster)

    if sprite.spritecollide(player,monsters,False):
        game = False
     
    if lost > lost_max:
        game = False
    
    if  score > 10:
        game = False
    
    player.update()
    monsters.update()
    display.update()
    bullets.update()
    clock.tick(60)