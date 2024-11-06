
from pygame import *
from random import randint
import sys
import os

init()

enemy_skip = 0

lives = 3

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(sprite_image).convert_alpha(), (size_x, size_y))
        self.speed = speed
        #каждый спрайт долен хранить сво-во rect - прямоугольник в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.mask = mask.from_surface(self.image)
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        global enemy_skip
        self.rect.y += self.speed
        if self.rect.y > 1020:
            self.rect.y = -50
            self.rect.x = randint(0, 1000)
            enemy_skip += 1

class Hearts(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, speed):
        super().__init__(sprite_image, sprite_x, sprite_y, size_x, size_y, speed)
        self.hearts = sprite.Group()
    def add_heart(self):
        self.hearts.add(self)

class Boss(GameSprite):
    def boss_update(self):
        self.rect.x += self.speed
        if self.rect.x > 850:
            self.rect.x = randint(0, 1000)

class Player(GameSprite):
    def control(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 850:
            self.rect.x += self.speed
        if keys[K_s] and self.rect.y < 850:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y > 150:
            self.rect.y -= self.speed
    def fire(self):
        bullet = Bullet('bullet_OneYear.png.png', self.rect.centerx -25, self.rect.y, 50, 100, 25)
        bullet_group.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()


true_fire = 50

enemy_num = 15

win_width = 1000
win_hight = 1000

window = display.set_mode((win_width, win_hight))

background = transform.scale(image.load('Background.png.png'), (win_width, win_hight))


player = Player('Sokol_OneThousYears-1.png.png', 390, 800, 150, 150, 3)

boss = Boss('DarthShip.png.png', 250, 0, 230, 200, 2)

x_heart = 350


hearts = GameSprite('heard.png', 350, 10, 50, 50, 0)
hearts_lives_group = sprite.Group()

hearts2 = GameSprite('heard.png', 450, 10, 50, 50, 0)
hearts3 = GameSprite('heard.png', 550, 10, 50, 50, 0)

hearts_lives_group.add(hearts)
hearts_lives_group.add(hearts2)
hearts_lives_group.add(hearts3)

bullet_group = sprite.Group()

enemy_group = sprite.Group()
for i in range(enemy_num):
    enemy = Enemy('Destroyer.png.png', randint(0,1000), randint(-200, -30), 100, 100, randint(1,2))
    enemy_group.add(enemy)

clock = time.Clock()
game = True
finish = False

destroyed = 0

font1 = font.Font(None, 50)
ships = font1.render('Cбито: ' + str(destroyed), True, (152, 0, 228))

mixer.music.load('Test_music_S-W.mp3')
mixer.music.set_volume(0.07)
mixer.music.play(-1)

bullet_sound = mixer.Sound('blaster.mp3')
bullet_sound.set_volume(0.07)

explotion = mixer.Sound('explotion_sound.mp3')
explotion.set_volume(0.07)

while game:
    moments = event.get()
    if finish != True:
        for ev in moments:
            if ev.type == QUIT:
                game = False
            elif ev.type == MOUSEBUTTONDOWN:
                if ev.button == 1:
                    if true_fire == 0:
                        bullet_sound.play()
                        player.fire()
                        true_fire = 50
        if true_fire > 0:
            true_fire -= 1
        collide = sprite.groupcollide(bullet_group, enemy_group, True, True, sprite.collide_mask)
        collide_player = sprite.spritecollide(player, enemy_group, False, sprite.collide_mask)
        if collide_player:
            finish = True
            mixer.music.stop()
        if collide:
            explotion.play()
            enemy_num -= 1
            destroyed += 1
            ships = font1.render('Cбито: ' + str(destroyed), True, (152, 0, 228))

        window.blit(background, (0, 0))
        window.blit(ships, (0, 10))
        player.reset()
        player.control()

        counter_enemy_skip = font1.render('Пропущено: ' + str(enemy_skip), True, (152, 0, 228))
        window.blit(counter_enemy_skip, (735, 10))

        bullet_group.draw(window)
        bullet_group.update()

        enemy_group.draw(window)
        enemy_group.update()

        hearts_lives_group.draw(window)

    for e1 in moments:
        if e1.type == QUIT:
            game = False
            finish = True
            sys.exit()

    display.update()
    clock.tick(120)
