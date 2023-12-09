import pygame
from pygame.locals import *
import random
from settings_frog import *

pygame.init()

class Player1(pygame.sprite.Sprite):
    """
    Classe responsável por inicializar o player de Frog Adventure e modificar seu estado

    Atributos:
    -----------
    - ``_visible`` (bool):
        Define se o sapo estará visível ou não.

    - ``_is_dead`` (bool):
        Define se o sapo está morto ou não (para a troca de sprites).

    - ``_speed`` (int):
        Define a velocidade do sapo.

    - ``image`` (pygame.Surface):
        Sprite do sapo.

    - ``rect`` (pygame.Rect):
        O retângulo que representa a posição e dimensões do sapo na tela.

    Métodos:
    --------
    - ``set_dead(self)``:
        Dá o sapo como morto e muda seu sprite.

    - ``set_alive(self)``:
        Faz o reespawn do sapo.

    Usos:
    -----
    frog = Player1()
    fg_gameover = True
    frog.set_dead()

    reset.game()
    frog.set_alive()

    """
    def __init__(self):
        """Essa função inicializa o player
        """
        super().__init__()
        self._visible = True
        self._is_dead = False
        self._speed = 6
        self.image = frog_img
        self.rect = self.image.get_rect()
        self.rect.center = [fg_player_x, fg_player_y]

    def set_dead(self):
        """Essa função seta o player como morto após colidir com um obstáculo
        """
        self._is_dead = True
        self.image = dead_frog

    def set_alive(self):
        """Essa função seta o player como vivo após recomeçar o jogo
        """
        self._is_dead = False
        self.image = frog_img
        self.rect = self.image.get_rect()
        self.rect.center = [640, 640]
    

class Obstacle(pygame.sprite.Sprite):
    """
    Classe responsável por inicializar os obstáculos do jogo Frog Adventure

    Atributos:
    -----------
    - ``image`` (pygame.Surface):
        Sprite dos obstáculos.

    - ``rect`` (pygame.Rect):
        O retângulo que representa a posição e dimensões dos obstáculos na tela.
    """
    def __init__(self, image, x, y):
        """Essa função inicializa os obstáculos do jogo
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class CollisionDetection:
    """
    Classe que abrange as colisões do jogo Frog Adventure

    Atributos:
    -----------
    - ``player`` (class):
        instância da classe Player1 (sapo).

    - ``obstacle_group`` (pygame.sprite.Group):
        Grupo de sprites dos obstáculos.

    Métodos:
    --------
    - ``check()``:
        checa se houve colisão entre o sapo e os obstáculos.

    Uso:
    ----
    frog = Player1
    check(frog, obstacle_group)
    
    """
    @staticmethod
    def check(player, obstacle_group):
        """Essa função checa se o jogador colidiu com um obstáculo
        """
        return pygame.sprite.spritecollide(player, obstacle_group, True)

class Background:
    """
    Classe responsável pelo controle do background do jogo Frog Adventure

    Atributos:
    -----------
    - ``__fg_background1`` (pygame.Surface):
        imagem 1 do background.

    - ``__fg_background2`` (pygame.Surface):
        imagem 2 do background.

    - ``background_image`` (pygame.Surface):
        imagem atual do background

    Métodos:
    --------
    - ``draw_background(self, screen)``:
        Desenha o background no jogo.

    Parâmetros:
    -----------
    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    Uso:
    ----
    background = Background()
    background.draw_background()
    """
    def __init__(self):
        """Essa função inicializa as duas imagens do background e a pontuação do jogador"
        """
        self.__fg_background1 = fg_background1
        self.__fg_background2 = fg_background2

    def draw_background(self, screen):
        """Essa função altera o background após um certo número de ticks
        """
        if pygame.time.get_ticks() % 2000 < 1000:
            background_image = self.__fg_background1
        else:
            background_image = self.__fg_background2
        screen.blit(background_image, (0, 0))

class Score: 
    """
    Classe responsável pelo controle do score do jogo Frog Adventure

    Atributos:
    -----------
    - ``__fg_score`` (int):
        score do player.

    - ``__fg_speed`` (int):
        velocidade dos obstáculos (sua atualização depende do score)

    - ``__font`` (pygame.Font):
        Fonte da escrita do score.

    - ``__text`` (str):
        O que estará escrito no score.

    - ``__text_rect`` (pygame.Rect):
        Rect do score.

    Método 1:
    --------
    - ``update_score(self))``:
        Essa função atualiza o jogador e aumenta a velocidade dos obtáculos a cada 5
        pontos

    Uso:
    -----
    score = Score()
    score.update_score()

    Método 2:
    --------
    - ``draw_score(self, screen)``:
        Desenha o score na tela

    Parâmetros:
    -----------
    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    Uso:
    ----
    score = Score()
    score.draw_score()
    """
    def __init__(self):
        """Essa função inicializa as duas imagens do background e a pontuação do jogador
        """
        self._fg_score = 0
        self._fg_speed = 2

    def update_score(self):
        """Essa função atualiza o jogador e aumenta a velocidade dos obtáculos a cada 5
        pontos
        """
        self._fg_score += 1
        if self._fg_score > 0 and self._fg_score % 5 == 0:
            self._fg_speed += 1

    def draw_score(self, screen):
        """Essa função deseja o score na tela

        Parâmetros:
        -----------
        - ``screen`` (pygame.Surface):
            Superfície da tela do jogo.

        """
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.__text = self.__font.render('Score: ' + str(self._fg_score), True, white)
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.center = (640, 40)
        screen.blit(self.__text, self.__text_rect)