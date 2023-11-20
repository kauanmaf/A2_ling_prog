import pygame
import sys
from random import randint
from settings import *
from overworld import Overworld
screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    def __init__(self) -> None:
        self.max_level = 3
        self.overworld = Overworld(0, self.max_level, screen)
    def run(self):
        self.overworld.run()

# Settingg up
pygame.init()
clock = pygame.time.Clock()
game = Game()

pygame.display.set_caption("joguinho")

#
# making the loop while to start
while True:
    clock.tick(200) 
    screen.fill((0,0,0))
    game.run()

    # Loop for para casa a pessoa queira sair do jogo 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fazendo um update pra manter no caso de atualizações
    pygame.display.update()