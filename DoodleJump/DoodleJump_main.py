import os
import sys
project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)

from abstract import Minigame_abs
from DoodleJump.settings_doodle import *
from DoodleJump.classes_base_doodle import *
import sys
import random

class DoodleJump(Minigame_abs):
    """
    Classe que representa o jogo Doodle Jump.

    Atributos:
    -----------
    - ``__screen`` (pygame.Surface):
        A superfície da tela do jogo.

    - ``__game_over`` (bool):
        Indica se o jogo terminou.

    - ``__platform_group`` (pygame.sprite.Group):
        O grupo de sprites contendo as plataformas.

    - ``__enemy_group`` (pygame.sprite.Group):
        O grupo de sprites contendo os inimigos.

    - ``__enemy_sheet`` (SpriteSheet):
        Uma instância da classe SpriteSheet para lidar com sprites de inimigos.

    - ``__jumpy`` (Jumper):
        Uma instância da classe Jumper representando o jogador.

    - ``__scroll`` (int):
        O valor de rolagem do jogo.

    - ``_background_scroll`` (int):
        O valor de rolagem do plano de fundo.

    - ``_score`` (int):
        A pontuação atual do jogador.

    - ``_fade_counter`` (int):
        Um contador para o efeito de desvanecimento.

    - ``_high_score`` (int):
        A pontuação mais alta do jogador.

    Métodos:
    --------
    - ``__init__(self, screen)``:
        Inicializa as variáveis necessárias para a criação do jogo.

    - ``create_background(self)``:
        Atualiza a rolagem do plano de fundo com base no valor de rolagem.

    - ``create_platforms(self)``:
        Cria plataformas com base em condições específicas e as adiciona ao grupo de plataformas.

    - ``draw_text(self, text, font, text_col, x, y)``:
        Desenha texto na tela do jogo com parâmetros específicos.

    - ``check_game_over(self)``:
        Verifica se o jogador está em um estado de jogo encerrado com base na posição e colisões.

    - ``create_enemies(self)``:
        Cria inimigos com base em condições específicas e os adiciona ao grupo de inimigos.

    - ``update_score(self)``:
        Atualiza a pontuação do jogador com base no valor de rolagem.

    - ``draw(self)``:
        Desenha vários elementos do jogo, incluindo o jogador, plataformas, inimigos e pontuação.

    - ``update(self)``:
        Atualiza as posições e estados de plataformas e inimigos com base no valor de rolagem.

    - ``draw_fade_counter(self)``:
        Desenha um efeito de desvanecimento na tela do jogo.

    - ``draw_game_over(self)``:
        Desenha a tela de fim de jogo com a pontuação do jogador e instruções para jogar novamente.

    - ``setting_high_score(self)``:
        Atualiza a pontuação mais alta se a pontuação atual a superar.

    - ``reset_game(self)``:
        Reseta o estado do jogo para um novo jogo se o jogador pressionar a tecla de espaço.

    - ``run(self)``:
        Executa o loop do jogo, lidando com a criação de elementos do jogo, desenho, atualização e estado de fim de jogo.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Inicializa as variáveis necessárias para a criação do jogo.
        """
        super().__init__()
        # Como todas as variáveis serão utilizadas apenas dentro dessa classe, podemos utiliza-las como atributos protegidos
        self.__screen = screen
        self.__game_over = False

        # Elaborando grupos de sprites
        self.__platform_group = pygame.sprite.Group()
        self.__enemy_group = pygame.sprite.Group()

        # Construindo a spritesheet do inimigo
        self.__enemy_sheet = SpriteSheet(enemy_sheet_image)
        # Criando a instância do jogador
        self.__jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.__platform_group)  
        
        self.__scroll = self.__jumpy.move()
        self._background_scroll = 0
        self._score = 0
        self._fade_counter = 0

        if os.path.exists("DoodleJump/score.txt"):
            with open("DoodleJump/score.txt", "r") as file:
                self._high_score = int(file.read())
        else:
            self._high_score = 0

    def create_background(self):
        """
        Atualiza a rolagem do plano de fundo com base no valor de rolagem.
        """
        self._background_scroll += self.__scroll

        # Desenha imagens de fundo com base no valor de rolagem
        self.__screen.blit(background_image, (0, 0 + self._background_scroll))
        self.__screen.blit(background_image, (0, -600 + self._background_scroll))

        # Verifica se a rolagem do plano de fundo ultrapassa o limite
        if self._background_scroll >= 600:
            # Reinicia a rolagem do plano de fundo
            self._background_scroll = 0

    def create_platforms(self):
        """
        Cria plataformas com base em condições específicas e as adiciona ao grupo de plataformas.
        """
        # Inserindo plataformas
        if not self.__platform_group:  
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
            self.__platform_group.add(platform)
        else:
            # Obtém a última plataforma no grupo
            last_platform = self.__platform_group.sprites()[-1]

            # Gera uma nova plataforma com base na posição da última plataforma
            platform_width = random.randint(40, 60)
            platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
            platform_y = last_platform.rect.y - random.randint(80, 120)
            platform_type = random.randint(1, 2)

            # Verificando as condições de movimentação das plataformas
            if platform_type == 1 and self._score > 750:
                platform_movement = True
            else:
                platform_movement = False

            platform = Platform(platform_x, platform_y, platform_width, platform_movement)
            self.__platform_group.add(platform)

    def draw_text(self, text, font, text_col, x, y):
        """
        Desenha texto na tela do jogo com parâmetros específicos.

        Parâmetros:
        -----------
        - ``text`` (str):
            O texto a ser exibido.

        - ``font`` (pygame.font.Font):
            O estilo da fonte para o texto.

        - ``text_col`` (tuple):
            A cor do texto.

        - ``x`` (int):
            A posição x do texto.

        - ``y`` (int):
            A posição y do texto.
        """
        text_image = font.render(text, True, text_col)
        self.__screen.blit(text_image, (x, y))

    def check_game_over(self):
        """
        Verifica se o jogo chegou ao fim, seja por tocar o topo da tela ou colidir com inimigos.
        """
        if self.__jumpy.rect.top > SCREEN_HEIGHT:
            self.__game_over = True
            death_sound.play()
        # Verificando se há colisão com inimigos
        if pygame.sprite.spritecollide(self.__jumpy, self.__enemy_group, False):
            if pygame.sprite.spritecollide(self.__jumpy, self.__enemy_group, False, pygame.sprite.collide_mask):
                self.__game_over = True
                death_sound.play()

    def create_enemies(self):
        """
        Cria inimigos no jogo com base na pontuação atual do jogador.
        """
        if len(self.__enemy_group) == 0 and self._score > 1500:
            enemy = Enemy(SCREEN_WIDTH, 100, self.__enemy_sheet, 1.5)
            self.__enemy_group.add(enemy)

    def update_score(self):
        """
        Atualiza a pontuação do jogador com base no deslocamento vertical.
        """
        if self.__scroll > 0:
            self._score += self.__scroll


    def draw(self):
        """
        Desenha os elementos do jogo na tela.
        """
        # Desenhando uma linha da pontuação maior
        pygame.draw.line(self.__screen, WHITE, (0, self._score - self._high_score + SCROLL_THRESH),
                         (SCREEN_WIDTH, self._score - self._high_score + SCROLL_THRESH), 3)
        self.draw_text("HIGH SCORE", font_small, WHITE, SCREEN_WIDTH - 130, self._score - self._high_score + SCROLL_THRESH)

        # Desenhando sprites do jogador
        self.__platform_group.draw(self.__screen)
        self.__enemy_group.draw(self.__screen)
        self.__jumpy.draw()

        # Desenhando o painel
        pygame.draw.rect(self.__screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
        pygame.draw.line(self.__screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
        self.draw_text("SCORE: " + str(self._score), font_small, WHITE, 0, 0)

    def update(self):
        """
        Atualiza o estado do jogo com base na entrada do usuário e colisões.
        """
        # Atualizando as plataformas e o inimigo
        self.__platform_group.update(self.__scroll)
        self.__enemy_group.update(self.__scroll)

    def draw_fade_counter(self):
        """
        Desenha o contador de desvanecimento na tela.
        """
        # Construindo o fundo da imagem de game over
        for rect_y in range(0, 6, 2):
            pygame.draw.rect(self.__screen, BLACK, (0, rect_y * 100, self._fade_counter, 100))
            pygame.draw.rect(self.__screen, BLACK, (SCREEN_WIDTH - self._fade_counter, (rect_y + 1) * 100, SCREEN_WIDTH, 100))

    def draw_game_over(self):
        """
        Desenha a tela de fim de jogo na tela.
        """
        # Inserindo textos à tela final
        self.draw_text("GAME OVER", font_big, WHITE, 130, 200) 
        self.draw_text("SCORE: " + str(self._score), font_big, WHITE, 130, 250) 
        self.draw_text("PRESS SPACE TO PLAY AGAIN", font_big, WHITE, 40, 300)  

    def setting_high_score(self):
        """
        Atualiza a pontuação mais alta se a pontuação atual a superar.
        """
        if self._score > self._high_score:
            self._high_score = self._score
            with open("DoodleJump/score.txt", "w") as file:
                file.write(str(self._high_score))

    def reset_game(self):
        """
        Reseta o estado do jogo para um novo jogo se o jogador pressionar a tecla de espaço.
        """
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # Redefinindo as variáveis
            self.__screen = screen
            self.__game_over = False
            self.__enemy_sheet = SpriteSheet(enemy_sheet_image)
            self.__platform_group = pygame.sprite.Group()
            self.__enemy_group = pygame.sprite.Group()
            self.__jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.__platform_group)
            self.__scroll = self.__jumpy.move()
            self._background_scroll = 0
            self.__game_over = False
            self._score = 0
            self._fade_counter = 0
            
            if os.path.exists("score.txt"):
                with open("DoodleJump/score.txt", "r") as file:
                    self._high_score = int(file.read())
            else:
                self._high_score = 0

    def run(self):
        """
        Executa o loop do jogo, lidando com início, reinício, desenho e atualização do jogo.
        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1, 0.0)
        if not self.__game_over:
            self.create_background()
            self.create_platforms()
            self.create_enemies()
            self.draw()
            self.__scroll = self.__jumpy.move() 
            self.update_score()
            self.update()
            self.check_game_over()
        else:
            if self._fade_counter < SCREEN_WIDTH:
                # Construindo o fundo da imagem de game over
                self.create_background()
                self._fade_counter += 5
                self.draw_fade_counter()
            else:
                self.draw_game_over()
                self.setting_high_score()
                self.reset_game()

    
    
if __name__ == "__main__":
    # Inicializando o pygame
    pygame.mixer.init()
    pygame.init()
    # Criando a janela do jogo
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Criando uma instância do jogo
    game = DoodleJump(screen)


    while True:
        # Configurando a taxa de atualização do jogo
        clock.tick(60)

        # Configurando o fundo da tela
        screen.fill((0, 0, 0))

        # Executando o jogo
        game.run()

        # Loop for caso a pessoa queira sair do jogo
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        # Fazendo um update pra manter no caso de atualizações
        pygame.display.update()
        
