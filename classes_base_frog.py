import pygame
from pygame.locals import *
import random
from settings_frog import *

pygame.init()

class Player1(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        """Essa função inicializa o player
        """
        super().__init__()
        self._visible = True
        self._is_dead = False
        self._speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def set_dead(self):
        """Essa função seta o player como morto após colidir com um obstáculo
        """
        self._is_dead = True
        self.image = dead_frog
        self.rect = self.image.get_rect()
        self.rect.center = [640, 640]

    def set_alive(self):
        """Essa função seta o player como vivo após recomeçar o jogo
        """
        self._is_dead = False
        self.image = frog_img
        self.rect = self.image.get_rect()
        self.rect.center = [640, 640]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        """Essa função inicializa os obstáculos do jogo
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class CollisionDetection:
    @staticmethod
    def check(player, obstacle_group):
        """Essa função checa se o jogador colidiu com um obstáculo
        """
        return pygame.sprite.spritecollide(player, obstacle_group, True)

class BackgroundAndScore:
    def __init__(self):
        """Essa função inicializa as duas imagens do background e a pontuação do jogador"
        """
        self.__fg_background1 = fg_background1
        self.__fg_background2 = fg_background2
        self.__fg_score = 0
        self._fg_speed = 2

    def update_score(self):
        """Essa função atualiza o jogador e aumenta a velocidade dos obtáculos a cada 5
        pontos
        """
        self.__fg_score += 1
        if self.__fg_score > 0 and self.__fg_score % 5 == 0:
            self._fg_speed += 1

    def draw_background(self, screen):
        """Esse função altera o background após um certo número de ticks
        """
        if pygame.time.get_ticks() % 2000 < 1000:
            background_image = self.__fg_background1
        else:
            background_image = self.__fg_background2
        screen.blit(background_image, (0, 0))

    def draw_score(self, screen):
        """Essa função deseja o score na tela
        """
        __font = pygame.font.Font(pygame.font.get_default_font(), 30)
        __text = __font.render('Score: ' + str(self.__fg_score), True, white)
        __text_rect = __text.get_rect()
        __text_rect.center = (640, 40)
        screen.blit(__text, __text_rect)