"""
Módulo criado para o esboço do jogo Flappy Bird.
Esse módulo contém as classes básicas do jogo Flappy Bird: Bird, Groud, Pipe, CollisionDetector e Menu.
"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)

import pygame
from FlappyBird.settings_flappy import *
from abstract import *

class Bird(Player):
    """
    Classe responsável pela criação e controle do pássaro no jogo FlappyBird.

    Atributos:
    -----------
    - ``image`` (pygame.Surface):
        A imagem que representa o pássaro.

    - ``rect`` (pygame.Rect):
        O retângulo que representa a posição e dimensões do pássaro na tela.

    - ``__image_index`` (int):
        O índice usado para a animação do pássaro.

    - ``__vel`` (float):
        A velocidade vertical do pássaro.

    - ``__flap`` (bool):
        Indica se o pássaro realizou um movimento de flap.

    - ``_alive`` (bool):
        Indica se o pássaro está vivo.

    Métodos:
    --------
    - ``update(user_input, y_pos_ground = 530)``:
        Atualiza o estado do pássaro com base na entrada do usuário.

    Parâmetros:
    - ``user_input`` (dict):
        Dicionário contendo o estado das teclas pressionadas pelo usuário.

    - ``y_pos_ground`` (int):
        Posição vertical do chão no jogo (padrão: 530).

    Uso:
    -----
    bird = Bird(bird_start_position)
    bird.update(user_input)
    """

    def __init__(self, bird_start_position : tuple):
        """
        Inicializa a classe Bird.

        Parâmetros:
        -----------
        - ``bird_start_position`` (tuple):
            Tupla com a posição inicial do pássaro (x,y).
        """
        super().__init__()
        # Inicialização dos atributos públicos
        self.image = bird_images_flappy[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.__image_index = 0
        self.__vel = 0
        self.__flap = False
        self._alive = True
    

    def update(self, user_input, y_pos_ground:int = 530):
        """
     - ``update(user_input, y_pos_ground=530)``:
        Atualiza o estado do pássaro com base na entrada do usuário.

    Parâmetros:
    - ``user_input`` (dict):
        Dicionário contendo o estado das teclas pressionadas pelo usuário.

    - ``y_pos_ground`` (int):
        Posição vertical do chão no jogo (padrão: 530)..
        """
        # Animação do pássaro
        if self._alive:
            self.__image_index += 1
        if self.__image_index >= 30:
            self.__image_index = 0
        self.image = bird_images_flappy[self.__image_index // 10]

        # Atualização da velocidade vertical
        self.__vel += 0.5
        if self.__vel > 7:
            self.__vel = 7
        if self.rect.bottom < y_pos_ground:
            self.rect.y += int(self.__vel)
        if self.__vel == 0:
            self.__flap = False

        # Verificação do flap
        if user_input[pygame.K_SPACE] and not self.__flap and self.rect.y > 0 and self._alive:
            self.__flap = True
            self.__vel = -7
            flap_sound_flappy.play()

        # Alteração da orientação do pássaro
        self.image = pygame.transform.rotate(self.image, self.__vel * -7)


class Ground(pygame.sprite.Sprite):
    """
    Classe responsável pela criação e controle do solo no jogo FlappyBird.

    Atributos:
    -----------
    - ``image`` (pygame.Surface):
        Superfície representando a imagem do solo.

    - ``rect`` (pygame.Rect):
        Retângulo representando a posição e dimensões do solo na tela.

    - ``__scroll_speed`` (int):
        Velocidade de deslocamento do solo.

    Métodos:
    --------
    - ``update()``:
        Atualiza a posição do solo com base na velocidade de deslocamento.

    Parâmetros:
    -----------
    - ``pos_x`` (int):
        Posição horizontal inicial do solo.

    - ``pos_y`` (int):
        Posição vertical inicial do solo.

    - ``scroll_speed`` (int):
        Velocidade de deslocamento do solo.

    Uso:
    -----
    ground = Ground(pos_x, pos_y, scroll_speed)
    ground.update()
    """
    def __init__(self, pos_x: int, pos_y: int, scroll_speed: int):
        """
        Inicializa a classe Ground.

        Parâmetros:
        -----------
        - ``pos_x`` (int):
            Posição horizontal inicial do solo.

        - ``pos_y`` (int):
            Posição vertical inicial do solo.

        - ``__scroll_speed`` (int):
            Velocidade de deslocamento do solo.
        """
        super().__init__()

        # Inicialização dos atributos públicos
        self.image = ground_image_flappy
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        # Inicialização de atributos privados
        self.__scroll_speed = scroll_speed

    def update(self):
        """
        Atualiza a posição do solo com base na velocidade de deslocamento.
        """
        self.rect.x -= self.__scroll_speed
        if self.rect.x <= -self.image.get_width():
            self.kill()


class Pipe(pygame.sprite.Sprite):
    """
    Classe responsável pela criação e controle dos canos no jogo FlappyBird.

    Atributos:
    -----------
    - ``image`` (pygame.Surface):
        Superfície representando a imagem do cano.

    - ``rect`` (pygame.Rect):
        Retângulo representando a posição e dimensões do cano na tela.

    - ``__scroll_speed`` (int):
        Velocidade de deslocamento do cano.

    - ``_pipe_type`` (str):
        Tipo de cano ("top" para o cano superior, "bottom" para o cano inferior).

    - ``_enter`` (bool):
        Indica se o pássaro entrou no espaço entre os canos.

    - ``_exit`` (bool):
        Indica se o pássaro saiu do espaço entre os canos.

    - ``_passed`` (bool):
        Indica se o pássaro passou pelos canos.

    Métodos:
    --------
    - ``update()``:
        Atualiza a posição do cano com base na velocidade de deslocamento.

    Parâmetros:
    -----------
    - ``pos_x`` (int):
        Posição horizontal inicial do cano.

    - ``pos_y`` (int):
        Posição vertical inicial do cano.

    - ``image`` (pygame.Surface):
        Superfície representando a imagem do cano.

    - ``pipe_type`` (str):
        Tipo de cano ("top" para o cano superior, "bottom" para o cano inferior).

    - ``scroll_speed`` (int):
        Velocidade de deslocamento do cano.

    Uso:
    -----
    pipe = Pipe(pos_x, pos_y, image, pipe_type, scroll_speed)
    pipe.update()
    """
    def __init__(self, pos_x: int, pos_y: int, image: pygame.Surface, pipe_type: str, scroll_speed: int):
        """
        Inicializa a classe Pipe

        Parâmetros:
        -----------
        - ``pos_x`` (int):
        Posição horizontal inicial do cano.

    - ``pos_y`` (int):
        Posição vertical inicial do cano.

    - ``image`` (pygame.Surface):
        Superfície representando a imagem do cano.

    - ``pipe_type`` (str):
        Tipo de cano ("top" para o cano superior, "bottom" para o cano inferior).

    - ``scroll_speed`` (int):
        Velocidade de deslocamento do cano.
        """
        super().__init__()

        # Inicialização de atributos públicos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        # Inicialização de atributos privados e protegidos
        self.__scroll_speed = scroll_speed
        self._pipe_type = pipe_type

        # Atributos relacionados à pontuação
        self._enter = False
        self._exit = False
        self._passed = False
    
    def update(self):
        """
        Atualiza a posição do cano com base na velocidade de deslocamento.
        """
        self.rect.x -= self.__scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()


class CollisionDetector:
    """
    Classe responsável pela detecção de colisões no jogo FlappyBird.

    Atributos:
    -----------
    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    - ``__bird`` (pygame.sprite.GroupSingle):
        Grupo de sprites contendo o pássaro.

    - ``__ground`` (pygame.sprite.Group):
        Grupo de sprites contendo o chão.

    - ``__pipes`` (pygame.sprite.Group):
        Grupo de sprites contendo os canos.

    Métodos:
    --------
    - ``check_collisions()``:
        Verifica e trata colisões entre o pássaro, o chão e os canos.

    Parâmetros:
    -----------
    - ``bird`` (pygame.sprite.GroupSingle):
        Grupo de sprites contendo o pássaro.

    - ``ground`` (pygame.sprite.Group):
        Grupo de sprites contendo o chão.

    - ``pipes`` (pygame.sprite.Group):
        Grupo de sprites contendo os canos.

    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    Uso:
    -----
    collision_detector = CollisionDetector(bird, ground, pipes, screen)
    collision_detector.check_collisions()
    """

    def __init__(self, bird: pygame.sprite.GroupSingle, ground: pygame.sprite.Group, 
                 pipes: pygame.sprite.Group, screen: pygame.Surface):
        """
        Inicializa a classe CollisionDetector.

        Parâmetros:
        -----------
        - ``screen`` (pygame.Surface):
            Superfície da tela do jogo.

        - ``bird`` (pygame.sprite.GroupSingle):
            Grupo de sprites contendo o pássaro.

        - ``ground`` (pygame.sprite.Group):
            Grupo de sprites contendo o chão.

        - ``pipes`` (pygame.sprite.Group):
            Grupo de sprites contendo os canos.

        - ``hit`` (bool):
            Verifica se o pássaro já colidiu com o chão alguma vez
        """
        self.screen = screen
        self.__bird = bird
        self.__ground = ground
        self.__pipes = pipes
        self.__hit = False
        

    def check_collisions(self):
        """
        Verifica e trata colisões entre o pássaro, o chão e os canos.
        """
        collision_ground = pygame.sprite.spritecollide(self.__bird.sprite, self.__ground, False)
        collision_pipes = pygame.sprite.spritecollide(self.__bird.sprite, self.__pipes, False)

        if collision_pipes or collision_ground:
            # Fazendo o som na primeira vez que ocorre a colisão 
            if self.__bird.sprite._alive:
                hit_sound_flappy.play()

            self.__bird.sprite._alive = False
            if collision_ground:
                # Fazendo o som da primeira vez que encosta no chão
                if not self.__hit:
                    die_sound_flappy.play()
                    self.__hit = True
                # Desenha a imagem de game over
                self.screen.blit(game_over_image_flappy,
                            (screen_width // 2 - game_over_image_flappy.get_width() // 2,
                             screen_height // 2 - game_over_image_flappy.get_height() // 2))
                


class Menu:
    """
    Classe responsável por gerenciar o menu inicial do jogo FlappyBird.

    Atributos:
    -----------
    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    - ``__bird_start_position`` (tuple):
        Posição inicial do pássaro.

    Métodos:
    --------
    - ``draw()``:
        Desenha o menu inicial na tela.

    Parâmetros:
    -----------
    - ``screen`` (pygame.Surface):
        Superfície da tela do jogo.

    - ``bird_start_position`` (tuple):
        Posição inicial do pássaro.

    Uso:
    -----
    menu = Menu(screen, bird_start_position)
    menu.draw()
    """

    def __init__(self, screen : pygame.Surface , bird_start_position: tuple):
        """
        Inicializa a classe Menu.

        Parâmetros:
        -----------
        - ``screen`` (pygame.Surface):
            Superfície da tela do jogo.

        - ``bird_start_position`` (tuple):
            Posição inicial do pássaro.
        """
        self.screen = screen
        self.__bird_start_position = bird_start_position

    def draw(self):
        """
        Desenha o menu inicial na tela.
        """
        self.screen.blit(skyline_image_flappy, (0, 0))
        self.screen.blit(ground_image_flappy, Ground(0, 520, 3).rect)
        self.screen.blit(ground_image_flappy, Ground(ground_image_flappy.get_width(), 520, 3).rect)

        self.screen.blit(bird_images_flappy[0], self.__bird_start_position)
        self.screen.blit(start_image_flappy, (screen_width // 2 - start_image_flappy.get_width() // 2,
                                       screen_height // 2 - start_image_flappy.get_height() // 2))