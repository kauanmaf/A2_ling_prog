import sys
import pygame
from settings import *
from level_map import Level_map
from minigame import *

screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    """
    Classe responsável por gerenciar a instância do jogo.

    :ivar int max_level: O nível máximo permitido no jogo.
    :ivar Level_map level_map: A instância do mapa de níveis.
    :ivar str status: O status atual do jogo ('level_map' ou 'minigame').

    :param int max_level: O nível máximo padrão ao inicializar o jogo.
    """
    def __init__(self, max_level=3):
        """
        Inicializa uma nova instância do jogo.

        :param int max_level: O nível máximo permitido no jogo.
        """

        self.max_level = max_level

        # Passamos a função create_minigame dentro de level_map para chama-la dentro de level_map e instanciar um jogo.
        self.level_map = Level_map(0, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def create_minigame(self, current_level):
        """
        Cria uma nova instância de Minigame.

        :param current_level: O nível atual para o Minigame.
        :type current_level: int

        :return: A instância do Minigame criada.
        :rtype: Minigame
        """
        self.minigame = Minigame(current_level, screen, self.level_map)
        self.status = "minigame"

    def create_level_map(self, current_level, new_max_level):
        """
        Cria uma nova instância de Level_map.

        :param current_level: O nível atual para o novo Level_map (int).
        :type current_level: int

        :param new_max_level: O novo nível máximo (int).
        :type new_max_level: int

        :return: A instância do novo Level_map criada.
        :rtype: Level_map
        """
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.level_map = Level_map(current_level, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def run(self):
        """
        Executa o loop do jogo com base no status atual.
        """
        if self.status == "level_map":
            self.level_map.run()
        else:
            self.minigame.run_minigame()