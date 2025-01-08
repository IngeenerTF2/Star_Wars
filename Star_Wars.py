
from pygame import *
from random import randint
import sys
from time import time as timer
import os

#! тестовый коммит
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
    '''движение босса влево/вправо, а так же резкое движение прямо
             с возвратом на исходную позицию(с целью тарана) + стрельба босса'''
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, speed):
        super().__init__(sprite_image, sprite_x, sprite_y, size_x, size_y, speed)
        self.derection = 'right'
        self.x1 = randint(30, 250)
        self.x2 = randint(300, 900)
    def update(self):
        if self.rect.x >= self.x2:
            self.derection = 'left'
            self.x1 = randint(30, 900)
        if self.rect.x <= self.x1:
            self.derection = 'right'
            self.x2 = randint(300, 900)
        if self.derection == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def fire_boss(self):
        enemy_and_boss_bullet = Bullet('Enemy_Bullet.png', self.rect.centerx -25, self.rect.centery, 50, 100, -25)
        enemy_bullet.add(enemy_and_boss_bullet)



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

class Explotion(sprite.Sprite):
    def __init__(self, x_enemy, y_enemy):
        super().__init__()
        self.images = []
        for num in range(1, 9):
            img = image.load(f"img/enemy_explotion{num}.png")
            img = transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x_enemy, y_enemy]
        self.counter = 0

    def update(self):
        explotion_speed = 4
        explotions.counter += 1

        if self.counter >= explotion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explotion_speed:
            self.kill()

class Boss_explotion(Explotion):
    def __init__(self, x_enemy, y_enemy):
        super().__init__(x_enemy = x_enemy, y_enemy = y_enemy )
        self.images = []
        for num in range(1, 11):
            img = image.load(f"boss_expl/boom{num}.png")
            img = transform.scale(img, (200, 200))
            self.images.append(img)

true_fire = 50
true_fire_boss = 10000

enemy_num = 3

lives_boss = 3

win_width = 1000
win_hight = 1000

window = display.set_mode((win_width, win_hight))

background = transform.scale(image.load('Background.png.png'), (win_width, win_hight))

you_lose = transform.scale(image.load('overtv.png'), (win_width, win_hight))

you_win = transform.scale(image.load('wintv.png'), (win_width, win_hight))

player = Player('Sokol_OneThousYears-1.png.png', 390, 800, 150, 150, 3)

boss = Boss('DarthShip.png.png', 250, 100, 230, 200, 2)

x_heart = 350

explotion_boss = sprite.Group()

hearts = GameSprite('heart_pixel.png', 10, 250, 150, 150, 0)
hearts_lives_group = sprite.Group()

hearts2 = GameSprite('heart_pixel.png', 10, 350, 150, 150, 0)
hearts3 = GameSprite('heart_pixel.png', 10, 450, 150, 150, 0)

hearts_lives_group.add(hearts)
hearts_lives_group.add(hearts2)
hearts_lives_group.add(hearts3)

bullet_group = sprite.Group()

enemy_bullet = sprite.Group()

enemy_group = sprite.Group()

player_group = sprite.Group()
player_group.add(player)

boss_group = sprite.Group()
boss_group.add(boss)

for i in range(enemy_num):
    enemy = Enemy('Destroyer.png.png', randint(0,1000), randint(-200, -30), 100, 100, randint(1,2))
    enemy_group.add(enemy)

clock = time.Clock()
game = True
finish = False

destroyed = 0

font1 = font.Font(None, 50)
ships = font1.render('Cбито: ' + str(destroyed), True, (152, 0, 228))

explotion_group = sprite.Group()

mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.07)
mixer.music.play(-1)

bullet_sound = mixer.Sound('blaster.mp3')
bullet_sound.set_volume(0.07)

lose_music = mixer.Sound('lose_music.mp3')
lose_music.set_volume(0.07)


explotion = mixer.Sound('explotion_sound.mp3')
explotion.set_volume(0.07)
start_time = timer()

x_enemy = 0
y_enemy = 0
'''def kill_boss(collide_boss_die):
    global x_enemy, y_enemy, explotions
    for i in collide_boss_die:
        x_enemy = i.rect.centerx
        y_enemy = i.rect.centery
    explotions = Explotion(x_enemy, y_enemy)
    explotion_group.add(explotions)'''

bullet_group_boss = sprite.Group()

while game:
    if lives <= 0:
        mixer.music.stop()
        finish = True
        window.blit(you_lose, (0, 0))

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
        collide = sprite.groupcollide(enemy_group, bullet_group, True, True, sprite.collide_mask)
        collide_player = sprite.spritecollide(player, enemy_group, False, sprite.collide_mask)

        collide_boss = sprite.spritecollide(player, boss_group, False, sprite.collide_mask)

        lives_collide = sprite.groupcollide(player_group, enemy_bullet, False, True, sprite.collide_mask)

        if lives_collide:
            lives -= 1



        if collide_boss:
            finish = True

        if collide_player:
            finish = True
            mixer.music.stop()
            #lose_music.play()
            mixer.music.load('lose_music.mp3')
            mixer.music.set_volume(0.07)
            mixer.music.play(-1)


        if collide:
            for i in collide:
                x_enemy = i.rect.centerx
                y_enemy = i.rect.centery
            explotions = Explotion(x_enemy, y_enemy)
            explotion_group.add(explotions)



        for col in collide:
            explotion.play()
            destroyed += 1
            enemy = Enemy('Destroyer.png.png', randint(50, 950), randint(-200, -30), 100, 100, randint(1, 2))
            enemy_group.add(enemy)
            ships = font1.render('Cбито: ' + str(destroyed), True, (152, 0, 228))

        window.blit(background, (0, 0))
        window.blit(ships, (0, 10))
        player.reset()
        player.control()

        

        counter_enemy_skip = font1.render('Пропущено: ' + str(enemy_skip), True, (152, 0, 228))
        window.blit(counter_enemy_skip, (735, 10))

        enemy_group.draw(window)
        enemy_group.update()

        bullet_group.draw(window)
        bullet_group.update()

        if destroyed >= 1 and lives_boss >= 1:
            collide_bullet_boss = sprite.groupcollide(boss_group, bullet_group, False, True, sprite.collide_mask)
            if collide_bullet_boss:
                lives_boss -= 1
            end_time = timer()
            '''отображение босса'''
            boss_group.draw(window)
            boss_group.update()
            #boss.fire_boss()
            if end_time - start_time >= 1:
                start_time = timer()
                bullet_sound.play()
                boss.fire_boss()
        elif lives_boss <= 1:
            collide_bullet_boss = sprite.groupcollide(boss_group, bullet_group, True, True, sprite.collide_mask)
            if collide_bullet_boss:
                lives_boss -= 1
            end_time = timer()
            '''отображение босса'''
            boss_group.draw(window)
            boss_group.update()
            #boss.fire_boss()
            if end_time - start_time >= 4:
                start_time = timer()
                bullet_sound.play()
                boss.fire_boss()
            if collide_bullet_boss:
                for i in collide_bullet_boss:
                    x_enemy = i.rect.centerx
                    y_enemy = i.rect.centery
                explotions = Boss_explotion(x_enemy, y_enemy)
                explotion_boss.add(explotions)
        explotion_boss.draw(window)
        explotion_boss.update()

        if lives_boss > 0:
            enemy_bullet.draw(window)
            enemy_bullet.update()

        hearts_lives_group.draw(window)
        explotion_group.draw(window)
        explotion_group.update()

    for e1 in moments:
        if e1.type == QUIT:
            game = False
            finish = True
            sys.exit()

    display.update()
    clock.tick(120)
