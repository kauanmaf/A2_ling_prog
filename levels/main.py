import pygame
import sys
from random import randint
from settings import *
from overworld import Overworld
from level import Level

screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        self.status = "overworld"


    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = "level"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()

# Settingg up
pygame.init()
clock = pygame.time.Clock()
game = Game()

pygame.display.set_caption("joguinho")

#
# making the loop while to start
while True:
    clock.tick(100) 
    screen.fill((0,0,0))
    game.run()

    # Loop for para casa a pessoa queira sair do jogo 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fazendo um update pra manter no caso de atualizações
    pygame.display.update()