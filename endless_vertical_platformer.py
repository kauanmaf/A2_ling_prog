import pygame
import random
from settings import *
from abstract import *
from utils import draw_background

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
            
        rect.center: tupla
            As coordenadas x e y do saltador
            
        vel_y: int
            A velocidade vertical do jogador
            
        flit: bool
            A rotação do saltador
            
    Métodos:
    --------
        move
            Realiza os movimentos do saltador
            
        draw
            Plota o saltador
        
    """
    def __init__(self, x, y ):
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
        
    def move(self):
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
        for platform in platform_group:
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
    """
    def __init__(self, x, y, width, movement):
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

        # Verifique seva plataforma saiu da tela
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
class SpriteSheet():
    def __init__(self, sheet_image):
        self.sheet = sheet_image
        
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(colour)
        
        return image
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
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