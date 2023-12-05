from enum import Enum

# Definindo as dimensões da tela do nosso jogo
screen_width = 1280
screen_height = 720

# Criando uma classe com cada minijogo e chamando pelo número
class Minigames_enum(Enum):
    "Classe com os jogos os quais iremos realizar."
    TETRIS = 0
    SPACE_INVADERS = 1
    PAC_MAN = 2
    FLAPPY_BIRD = 3

print(Minigames_enum.FLAPPY_BIRD.value == Minigames_enum.TETRIS.value + 3) 