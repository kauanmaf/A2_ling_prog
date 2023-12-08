import pygame
from settings import *
from abstract import *   

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

        # Verificando a colisão com o solo
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = - 20
            
        # Atualizando a posição do retângulo
        self.rect.x += dx
        self.rect.y += dy    

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 13, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)