"""
Módulo criado para o esboço do jogo Doodle Jump.
Esse módulo contém as classes básicas do jogo Doodle Jump: Jumper, Platform, SpriteSheet e Enemy.
"""

import os
import sys
project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)

import pygame
import random
from DoodleJump.settings_doodle import *
from abstract import *

class Jumper(Player):
    """
    A classe tem como objetivo criar e controlar o saltador do jogo
    
    Atributos:
    ----------
        image: pygame.Surface
            A imagem que representa o saltador
        
        width: int
            A largura do saltador
            
        height: int
            A altura do saltador
            
        rect: pygame.Rect
            O retângulo que contém a posição e a dimensão do saltador
            
        rect.center: tuple
            As coordenadas x e y do saltador
            
        vel_y: int
            A velocidade vertical do jogador
            
        flip: bool
            A rotação do saltador
            
    Métodos:
    --------
        move
            Realiza os movimentos do saltador
            
        draw
            Plota o saltador
        
    """
    def __init__(self, x, y, platform_group):
        """
        Inicializa a classe Jumper
            
        Parâmetros:
        -----------
            x: int
                Coordenada x do saltador

            y: int
                Coordenada y do saltador    
        """
        self.image = pygame.transform.scale(jumper_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        self.platform_group = platform_group

        
    def update(self):
        """
        A função realiza os movimentos horizontais e verticais do jogador
        
        Retorno:
        --------
            scroll: int
                rolagem da imagem            
        """
        # Redefinindo variáveis
        scroll = 0
        dx = 0
        dy = 0
        
        # Posicionando as teclas
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = - 10
            self.flip = False
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = True

        # Configurando a gravidade
        self.vel_y += GRAVITY    
        dy += self.vel_y

        # Garantindo que o player não saia da borda da tela
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
            
        # Averigando a colisão com as plataformas
        for platform in self.platform_group:
            # Colisão na direção y
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Verificando se está acima da plataforma
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = - 20

        # Verificando se o jogador saltou para o topo da tela
        if self.rect.top <= SCROLL_THRESH:
            # Averiguando se o jogador está pulando
            if self.vel_y < 0:  
                scroll = - dy
            
        # Atualizando a posição do retângulo
        self.rect.x += dx
        self.rect.y += dy + scroll
        
        # Atualizando a máscara
        self.mask = pygame.mask.from_surface(self.image)
        
        return scroll   

    def draw(self):
        """
        A função desenha o saltador
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 13, self.rect.y - 5))
        
class Platform(pygame.sprite.Sprite):
    """
    A classe é responsável pela criação e atualização das plataformas do jogo
    
    Atributos:
    ----------
        image: pygame.Surface
            A imagem da plataforma
            
        movement: bool
            A mobilidade da plataforma
            
        move_counter: int
            O contador de movimento
            
        direction: int
            O sentido da direção horizontal da plataforma
            
        speed: int
            A velocidade da plataforma
            
        rect: pygame.Rect
            O retângulo que possui a posição e a dimensão da plataforma
            
        rect.x: int
            A coordenada x do retângulo
            
        rect.y: int
            A coordenada y do retângulo
            
    Método:
    --------
        update(scroll)
            Movimenta e atualiza as plataformas com base na variável de rolagem
    """
    def __init__(self, x, y, width, movement):
        """
        Inicializa a classe Platform
        
        Parâmetros:
        -----------
            x: int
                Coordenada x da plataforma
            
            y: int
                Coordenada y da plataforma

            width: int 
                A largura da plataforma
            
            movement: bool
                O estado da plataforma
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.movement = movement
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([1, - 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, scroll):
        """
        A função realiza os movimentos das plataformas e atualiza o grupo de plataformas
        
        Parâmetro:
        ----------
            scroll: int
                A taxa de rolagem vertical da plataforma
        """
        # Movendo a plataforma de um lado para o outro se for uma plataforma móvel
        if self.movement == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
           
        # Mudando a direção da plataforma se ela fizer o movimento completo ou colidir com a parede
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= - 1
            self.move_counter = 0
        
        # Atualizando a posição vertical das plataformas
        self.rect.y += scroll 

        # Verifique se a plataforma saiu da tela
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
class SpriteSheet():
    """
    A classe tem como objetivo criar e obter sprites

    Atributos:
    ----------
        sheet: pygame.Surface
            A imagem utilizada na construção dos sprites
            
    Método:
    -------
        get_image(frame, width, height, scale, colour)
            Obtém sprites de uma imagem 
    """
    def __init__(self, sheet_image):
        """
        Inicializa a classe SpriteSheet
        
        Parâmetros:
        -----------
            sheet: pygame.Surface
                A imagem utilizada na confecção dos sprites
        """
        self.sheet = sheet_image
        
    def get_image(self, frame, width, height, scale, colour):
        """
        A função obtém os sprites de uma determinada imagem
        
        Parâmetros:
        -----------
            frame: pygame.Surface
                O quadro da imagem
                
            width: int
                A largura do sprite
                
            height: int
                A altura do sprite
                
            scale: float
                A escala do sprite
                
            colour: tuple
                O código da cor, no sistema RGB, considerada como transparente 
                
        Retorno:
        --------
            image: pygame.Surface
                Retorna o quadro da imagem
        """
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(colour)
        
        return image
        
class Enemy(pygame.sprite.Sprite):
    """
    A classe é responsável pela criação e atualização do inimigo no jogo
    
    Atributos:
    ----------
        animation: list
            A lista das animações do inimigo
        
        frame_index: int
            O índice referente ao quadro de animação
        
        update_time: pygame.time
            O instante da atualização do quadro
        
        direction: int
            O sentido da direção horizontal do inimigo
        
        flip: bool
            A rotação do inimigo
        
        image: pygame.Surface
            O quadro da imagem do inimigo
        
        rect: pygame.Rect
            O retângulo que contém a dimensão e a posição do inimigo
            
    Método:
    -------
        update(scroll)
            Movimenta e atualiza o inimigo com base na variável de rolagem
    """
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        """
        Inicializa a classe Enemy
        
        Parâmetros:
        -----------
            SCREEN_WIDTH: int
                A largura da janela do jogo
            
            y: int
                A coordenada y do inimigo
            
            sprite_sheet: pygame.Surface
                O sprite do inimigo
            
            scale: int
                A escala do sprite referente ao inimigo
        """
        pygame.sprite.Sprite.__init__(self)
        # Definindo variáveis
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        self.direction = random.choice([1, - 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False
            
        # Carregando imagens da spritesheet
        animation_steps = 8
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        # Selecionando uma imagem inicial e criando um retângulo por meio da figura    
        self.image = self.animation_list[self.frame_index] 
        self.rect = self.image.get_rect()
               
        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH
        self.rect.y = y
        
    def update(self, scroll):
        """
        A função movimenta e atualiza o inimigo
        
        Parâmetro:
        ----------
            scroll: int
                A taxa de rolagem vertical do inimigo
        """
        # Atualizando a animação
        ANIMATION_COOLDOWN = 60
        # Atualizando a imagem dependendo do quadro atual
        self.image = self.animation_list[self.frame_index]
        # Verificando se passou tempo suficiente desde a última atualização
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        # Reiniciando o índice de quadros quando a animação chega ao fim
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
        # Movendo o inimigo
        self.rect.x += self.direction * 2
        self.rect.y += scroll
        
        # Verificando se o inimigo saiu da tela
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()