import pygame
import random
from settings import *
from abstract import *
from utils import draw_background

class Jumper(Player):
    def __init__(self, x, y ):
        self.image = pygame.transform.scale(jumper_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        
    def move(self):
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
        
        return scroll   

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 13, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
class Platform(pygame.sprite.Sprite):
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
        self.direction = random.choice([1, - 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False
        # Carregando imagens da spritesheet
        image = sprite_sheet.get_image(0, 32, 32, scale, (0, 0, 0))
        image = pygame.transform.flip(image, self.flip, False)
        image.set_colorkey((0, 0, 0))
        self.image = image 
        self.rect = self.image.get_rect()       
        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH
        self.rect.y = y
        
    def update(self):
        # Movendo o inimigo
        self.rect.x += self.direction * 2
        # Verificando se o inimigo saiu da tela
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()