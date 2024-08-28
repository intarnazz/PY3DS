import pygame
import sys
from image import *


class Box:
    def __init__(self, screen, img="default", scale=()):
        self.screen = screen
        self.s_width = screen.get_rect()[2]
        self.s_height = screen.get_rect()[3]
        self.image = Image(img, scale)
        self.rect = self.image.get().get_rect()

    def blit(self):
        self.screen.blit(self.image.get(), self.rect)


class BG(Box):
    def __init__(self, screen):
        self.s_width = screen.get_rect()[2]
        self.s_height = screen.get_rect()[3]
        super().__init__(screen, "bg", (self.s_width, self.s_height))


class HpBar(Box):
    def __init__(self, screen, hero, x, y):
        super().__init__(screen, "hp_bar", (hero.hp * 3.82, 32))
        self.rect.x = x + 119
        self.rect.y = y + 59


class HpBarBorder(Box):
    def __init__(self, screen, hero):
        super().__init__(screen, "hp_bar_border")
        self.screen = screen
        self.hero = hero
        self.rect.y = self.hero.rect.top - 120
        self.rect.x = self.hero.rect.left - 100

    def hpBar(self):
        return HpBar(self.screen, self.hero, self.rect.x, self.rect.y)


class Hero(Box):
    def __init__(self, screen):
        super().__init__(screen, "hero", (300, 300))
        self.hp = 75
        self.rect.y = (self.s_height / 2) - (self.rect.height / 2)
        self.rect.x = 200


class Enemy(Box):
    def __init__(self, screen):
        super().__init__(screen, "enemy", (300, 300))
        self.hp = 20
        self.rect.y = (self.s_height / 2) - (self.rect.height / 2)
        self.rect.x = self.s_width - (200 + self.rect.width)


class Cart(Box):
    def __init__(self, screen):
        super().__init__(screen, "cart", (200, 300))
        self.rect.y = self.s_height - 300
        self.rect.x = 300


class MoveBox(Box):
    def __init__(self, screen, speed):
        super().__init__(screen, "cart", (200, 300))
        self.speed = speed
        self.box_up = False
        self.box_down = False
        self.box_right = False
        self.box_left = False
        self.rect.x = (self.s_width / 2) - (self.rect.width / 2)
        self.rect.y = (self.s_height / 2) - (self.rect.height / 2)

    def move_box(self):
        if self.box_up == True and self.rect.y > 0:
            self.rect.y -= self.speed
        if self.box_down == True and self.rect.y < self.s_height - self.rect.height:
            self.rect.y += self.speed
        if self.box_right == True and self.rect.x < self.s_width - self.rect.width:
            self.rect.x += self.speed
        if self.box_left == True and self.rect.x > 0:
            self.rect.x -= self.speed


class Focus(Box):
    def __init__(self, screen):
        super().__init__(screen, scale=(206, 306))
        self.rect.y = self.s_height - 300 - 3
        self.rect.x = 300 - 3
