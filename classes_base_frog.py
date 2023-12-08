import pygame
from pygame.locals import *
import random
from settings_frog import *

pygame.init()

class Player1(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.visible = True
        self.is_dead = False
        self.speed = 6
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def set_dead(self):
        self.is_dead = True
        self.image = dead_frog
        self.rect = self.image.get_rect()
        self.rect.center = [640, 640]

    def set_alive(self):
        self.is_dead = False
        self.image = frog_img
        self.rect = self.image.get_rect()
        self.rect.center = [640, 640]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class CollisionDetection:
    @staticmethod
    def check(player, obstacle_group):
        return pygame.sprite.spritecollide(player, obstacle_group, True)

class BackgroundAndScore:
    def __init__(self):
        self.fg_background1 = fg_background1
        self.fg_background2 = fg_background2
        self.fg_score = 0

    def update_score(self):
        self.fg_score += 1
        if self.fg_score > 0 and self.fg_score % 5 == 0:
            fg_speed += 1

    def draw_background(self, screen):
        if pygame.time.get_ticks() % 2000 < 1000:
            background_image = self.fg_background1
        else:
            background_image = self.fg_background2
        screen.blit(background_image, (0, 0))

    def draw_score(self, screen):
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render('Score: ' + str(self.fg_score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (640, 40)
        screen.blit(text, text_rect)