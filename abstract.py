#"Arquivo que define as classes gerais as quais serão usadas"

import pygame
from abc import ABC, abstractmethod


class Minigame_abs(ABC):
    "Classe abstrata que serve para todos os minigames"

    def update(self):
        "Atualiza o estado do minijogo a cada quadro"
        ...

    def draw(self, screen):
        "Desenha elementos do minijogo na tela"
        ...

    def run(self):
        "Função que serve para executar a classe o jogo"
        ...


class Player(ABC, pygame.sprite.Sprite):
    "Classe abstrata que serve para todos os players do jogo"

    def __init__(self):
        "Serve para iniciar o jogo"
        super().__init__()

    @abstractmethod
    def update(self): 
        "Serve para atualizar quando algo acontece com o player"
        ...