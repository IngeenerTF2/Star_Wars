
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
        self.flag = True
        self.x1 = randint(30, 250)
        self.x2 = randint(300, 900)
        self.ram_speed = 10
    def update(self):
        if self.flag and self.rect.y <= 100:
            if self.rect.x >= self.x2:
                self.derection = 'left'
                self.x1 = randint(0, 500)
            if self.rect.x <= self.x1:
                self.derection = 'right'
                self.x2 = randint(600, 1000)
            if self.derection == 'right':
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

    def fire_boss(self):
        enemy_and_boss_bullet = Bullet('Enemy_Bullet.png', self.rect.centerx -25, self.rect.centery, 50, 100, -25)
        enemy_bullet.add(enemy_and_boss_bullet)



    def ram(self):
        if not self.flag:
            self.rect.y += self.ram_speed
            if self.rect.y >= 700:
                self.flag = True

    def comeback(self):
        if self.flag and self.rect.y >= 100:
            self.rect.y -= self.speed


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
        self.counter += 1

        if self.counter >= explotion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explotion_speed:
            self.kill()

class Boss_explotion(Explotion):
    def __init__(self, x_enemy, y_enemy):
        super().__init__(x_enemy = x_enemy, y_enemy = y_enemy)
        self.images = []
        for num in range(1, 11):
            img = image.load(f"boss_expl/boom{num}.png")
            img = transform.scale(img, (200, 200))
            self.images.append(img)

class Heard_explotion(sprite.Sprite):
    def __init__(self, x_enemy, y_enemy):
        super().__init__()
        self.images = []
        for num in range(2, 9):
            img = image.load(f"crashed_heard/heard{num}.png")
            img = transform.scale(img, (200, 200))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x_enemy, y_enemy]
        self.counter = 0
    def update(self):
        explotion_speed = 10
        self.counter += 1

        if self.counter >= explotion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explotion_speed:
            self.kill()

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

boss = Boss('DarthShip.png.png', 250, 100, 230, 200, 3)

explotion_boss = sprite.Group()

hearts_list = []
heart_y = 250

for i in range(3):
    heart = GameSprite('crashed_heard/heard1.png', 10, heart_y, 150, 150, 0)
    hearts_list.append(heart)
    heart_y += 165

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

heart_group_explotion = sprite.Group()

mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.07)
mixer.music.play(-1)

bullet_sound = mixer.Sound('blaster.mp3')
bullet_sound.set_volume(0.07)

lose_music = mixer.Sound('lose_music.mp3')
lose_music.set_volume(0.07)


explotion = mixer.Sound('sound_explotion.ogg')
explotion.set_volume(0.07)
start_time = timer()
ram_time_start = timer()

x_enemy = 0
y_enemy = 0

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
        #соприкосновение пули и игрока
        lives_collide = sprite.groupcollide(player_group, enemy_bullet, False, True, sprite.collide_mask)

        if collide_boss:
            finish = True

        if collide_player:
            finish = True
            mixer.music.stop()
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
            ram_time = timer()
            '''отображение босса'''
            boss_group.draw(window)
            boss_group.update()
            if end_time - start_time >= 1:
                start_time = timer()
                bullet_sound.play()
                boss.fire_boss()

            if ram_time - ram_time_start >= 5:
                boss.flag = False
                if boss.rect.y <= 100:
                    ram_time_start = timer()
            boss.ram()
            boss.comeback()

        elif lives_boss <= 1:
            collide_bullet_boss = sprite.groupcollide(boss_group, bullet_group, True, True, sprite.collide_mask)
            if collide_bullet_boss:
                lives_boss -= 1
            end_time = timer()
            '''отображение босса'''
            boss_group.draw(window)
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

        explotion_group.draw(window)
        explotion_group.update()

        if lives_boss > 0:
            enemy_bullet.draw(window)
            enemy_bullet.update()

        for i in range(len(hearts_list)):
            hearts_list[i].reset()
        if lives_collide:
            x_heart = hearts_list[0].rect.centerx
            y_heart = hearts_list[0].rect.centery
            hearts_list.remove(hearts_list[0])
            heart_anim = Heard_explotion(x_heart, y_heart)
            heart_group_explotion.add(heart_anim)
            lives -= 1
        heart_group_explotion.draw(window)
        heart_group_explotion.update()

    for e1 in moments:
        if e1.type == QUIT:
            game = False
            finish = True
            sys.exit()

    display.update()
    clock.tick(120)
