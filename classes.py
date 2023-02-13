import random
import pygame
from pygame.locals import *


class Rocket(pygame.sprite.Sprite):
    """
    этот класс отвечает за спрайт игрока(космолёт), т.е обрабатывает нажатие кнопок управления и осуществляет движение
    спрайта
    """

    def __init__(self, size):
        super(Rocket, self).__init__()
        self.width, self.height = size
        self.surf = pygame.image.load('rocket.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(250, self.height * 0.50))
        self.speed = 5
        self.dirlist = ['top', 'right', 'bottom', 'left']
        self.dirindex = 0
        self.comms = self.dirlist[self.dirindex]

    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

    def rotate_left(self):
        self.dirindex -= 1
        if self.dirindex < -3:
            self.dirindex = 0
        self.comms = self.dirlist[self.dirindex]
        self.rotate_center(90)

    def rotate_right(self):
        self.dirindex += 1
        if self.dirindex > 3:
            self.dirindex = 0
        self.comms = self.dirlist[self.dirindex]
        self.rotate_center(-90)

    def rotate_center(self, angle):
        orig_rect = self.surf.get_rect()
        rot_image = pygame.transform.rotate(self.surf, angle)
        self.rot_rect = orig_rect.copy()
        self.rot_rect.center = rot_image.get_rect().center
        self.surf = rot_image.subsurface(self.rot_rect).copy()


class Bullet(pygame.sprite.Sprite):
    """
    этот класс отвечает за спрайты выстрелов ракеты(смена внешнего вида пули, ёё перемещение на игровом поле и удаление
    спрайта, когда он находится за границами поля)
    """

    def __init__(self, pos, dir_, size):
        super(Bullet, self).__init__()

        self.pos = pos
        self.dir = dir_
        self.width, self.height = size

        img_sp = [f'bullets/b{i}.png' for i in range(1, 11)]
        bullet = random.choice(img_sp)

        self.surf = pygame.image.load(bullet).convert()
        self.surf.set_colorkey((0, 0, 0))

        position = self.get_bullet_pos(self.pos)
        self.rect = self.surf.get_rect(center=position)

    def get_bullet_pos(self, pos):
        if self.dir == 'top':
            pos = (pos[0] + 32, pos[1] - 10)
        elif self.dir == 'left':
            pos = (pos[0] - 10, pos[1] + 32)
        elif self.dir == 'right':
            pos = (pos[0] + 74, pos[1] + 32)
        elif self.dir == 'bottom':
            pos = (pos[0] + 32, pos[1] + 74)

        return pos

    def update(self):
        if self.dir == 'top':
            self.rect.move_ip(0, -5)
            if self.rect.bottom < 0:
                self.kill()
        elif self.dir == 'left':
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
        elif self.dir == 'bottom':
            self.rect.move_ip(0, 5)
            if self.rect.top > self.height:
                self.kill()
        elif self.dir == 'right':
            self.rect.move_ip(5, 0)
            if self.rect.left > self.width:
                self.kill()


class Asteroid(pygame.sprite.Sprite):
    """
    этот класс осуществляет создание, перемещение и удаление с игрового поля спрайта астероида
    """

    def __init__(self, type, size):
        super(Asteroid, self).__init__()

        self.width, self.height = size
        asteroid_sp = {i: f'asteroids/asteroid{i}.png' for i in range(1, 6)}
        img = asteroid_sp.get(type)
        self.dirlist = ['top', 'bottom', 'left', 'right']
        self.dir = random.choice(self.dirlist)
        self.surf = pygame.image.load(img).convert()
        self.surf.set_colorkey((0, 0, 0))
        pos = self.initial_pos()
        if self.dir in ('top', 'bottom'):
            if pos[0] < self.width / 2:
                self.x = random.choice([0, 0, 0, 1, 2, 3, 4, 5])
            elif pos[0] >= self.width / 2:
                self.x = random.choice([0, 0, 0, -1, -2, -3, -4, -5])
        elif self.dir in ('left', 'right'):
            if pos[1] < self.height / 2:
                self.y = random.choice([0, 0, 0, 1, 2, 3, 4, 5])
            elif pos[1] >= self.height / 2:
                self.y = random.choice([0, 0, 0, -1, -2, -3, -4, -5])
        self.rect = self.surf.get_rect(center=pos)

    def initial_pos(self):
        if self.dir == 'top':
            pos = (
                random.randint(20, self.width - 20),
                -random.randint(50, 150)
            )
        elif self.dir == 'bottom':
            pos = (
                random.randint(20, self.width - 20),
                random.randint(self.height + 50, self.height + 100)
            )
        elif self.dir == 'left':
            pos = (
                random.randint(-20, 0),
                random.randint(0, self.height)
            )
        elif self.dir == 'right':
            pos = (
                random.randint(self.width + 20, self.width + 70),
                random.randint(0, self.height)
            )

        return pos

    def update(self):
        if self.dir == 'top':
            self.rect.move_ip(self.x, 5)
            if self.rect.top > self.height:
                self.kill()
        elif self.dir == 'bottom':
            self.rect.move_ip(self.x, -5)
            if self.rect.bottom < 0:
                self.kill()
        elif self.dir == 'left':
            self.rect.move_ip(5, self.y)
            if self.rect.left > self.width:
                self.kill()
        elif self.dir == 'right':
            self.rect.move_ip(-5, self.y)
            if self.rect.right < 0:
                self.kill()


class Explosion(pygame.sprite.Sprite):
    """
    с помощью этого класса осуществляется анимация спрайта взрыва после уничтожения астероида
    """

    def __init__(self, pos):
        super(Explosion, self).__init__()
        self.images = []
        for i in range(17):
            file = f'explosion/Explosion{i}.png'
            image = pygame.image.load(file)
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.images[0].get_rect(center=pos)

    def update(self):
        self.index += 1
        if self.index > len(self.images) - 2:
            self.kill()
        self.image = self.images[self.index]
