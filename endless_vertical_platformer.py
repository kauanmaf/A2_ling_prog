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

        # Verificando a colisão com o solo
        if self.rect.bottom + dy > SCREEN_HEIGHT:
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
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, scroll):
       # Atualizando a posição vertical das plataformas
       self.rect.y += scroll  
            
        
# Elaborando grupos de sprites
platform_group = pygame.sprite.Group()

# Criando plataformas temporárias
for random_platform in range(MAX_PLATFORMS):
    random_platform_width = random.randint(40, 60)
    random_platform_x = random.randint(0, SCREEN_WIDTH - random_platform_width)
    random_platform_y = random_platform * random.randint(80, 120) - 700
    platform = Platform(random_platform_x, random_platform_y, random_platform_width)
    platform_group.add(platform)
