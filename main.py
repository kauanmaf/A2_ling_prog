import sys
import pygame
from settings import *
from level_map import Level_map
from minigame import *

screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    def __init__(self):
        self.max_level = 3
        self.level_map = Level_map(0, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def create_minigame(self, current_level):
        self.minigame = Minigame(current_level, screen, self.level_map)
        self.status = "minigame"

    def create_level_map(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.level_map = Level_map(current_level, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def run(self):
        if self.status == "level_map":
            self.level_map.run()
        else:
            self.minigame.run_minigame()


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