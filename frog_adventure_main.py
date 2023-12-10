from settings_frog import *
import pygame
from classes_base_frog import *
from pygame.locals import *
from abstract import Minigame_abs
import sys

class FrogJourneyGame(Minigame_abs):
    """
    Uma classe representando o jogo Frog Adventure
    
    Atributos:
    ----------
    - ``__player`` (Player1):
        Instância da classe Player1.

    - ``__collision_detection`` (CollisionDetection):
        Instância da classe CollisionDetection.

    - ``__score`` (Score):
        Instância da classe Score.

    - ``__background`` (Background):
        Instância da classe Background.

    - ``__player_group`` (pygame.sprite.Group):
        Grupo que contém o sprite do player.

    - ``__obstacle_group`` (pygame.sprite.Group):
        Grupo de contém os sprites dos objetos.

    - ``__fg_target_lane`` (int):
        coordenada da lane para qualo player deseja se movimentar.

    - ``__fg_gameover`` (bool):
        Utilizada para ações quando o player perde.

    - ``__fg_speed`` (int):
        Velocidade dos obstáculos.

    - ``__clock`` (pygame.time):
        método para controle dos ticks.

    - ``__running`` (bool):
        Variável que será True caso o jogo esteje rodando.

    Métodos:
    --------
    - ``run(self)``:
        Essa função abriga o loop que roda o jogo.

    - ``handle_events(self)``:
        Essa função controla os eventos de fechamento do jogo e aperto de teclas.    

    - ``update(self)``:
        Função que atualiza os aspectos do jogo a cada quadro.    

    - ``move_obstacles(self)``:
        Função que garante a movimentação dos obstáculos.

    - ``check_collisions(self)``:
        Função que detecta colisões e realiza ações a respeito.

    - ``render(self)``:
        Função que renderiza o jogo.

    - ``reset_game(self)``:
        Função que define aspectos do jogo ao ser resetado
    """
    def __init__(self):
        """Essa função inicializa as classes importadas e cria variáveis necessárias 
        para o funcionamento do jogo
        """

        #criando instancias das classes
        self.__player = Player1()
        self.__collision_detection = CollisionDetection()
        self.__background = Background()
        self.__score = Score()

        #criando sprite groups para o player
        self.__player_group = pygame.sprite.Group()
        self.__player_group.add(self.__player)
        self.__obstacle_group = pygame.sprite.Group()

        self.__obstacles = Obstacle(image, lane, screen_height / -2)

        #criando o restante dos atributos necessários para o jogo
        self.__fg_gameover = False
        self.__clock = pygame.time.Clock()
        self.__running = True
        
    def run(self):
        """Essa função abriga o loop que roda o jogo
        """
        while self.__running:
            self.__clock.tick(100)
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        """Essa função controla os eventos de fechamento do jogo e aperto de teclas
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            #Determinaremos a target_lane do player
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT and self.__player.rect.center[0] > left_lane:
                    self.__player._target_lane = left_lane
                elif event.key == K_RIGHT and self.__player.rect.center[0] < right_lane:
                    self.__player._target_lane = right_lane
                   

    def update(self):
        """Função que atualiza os aspectos do jogo a cada quadro.
        """
        Obstacle.draw_obstacles(self.__obstacle_group)
        self.__player.move_player()
        self.move_obstacles()
        self.check_collisions()

    def move_obstacles(self):
        """Função que garante a movimentação dos obstáculos
        """
        for obstacle in self.__obstacle_group:
            obstacle.rect.y += self.__score._fg_speed
            if obstacle.rect.top >= screen_height:
                obstacle.kill()
                self.__score.update_score()
                #obstaculo é eliminado se sair da tela e é adicionado 1 no score
    
    def check_collisions(self):
        """Função que detecta colisões e realiza ações a respeito
        """
        if self.__collision_detection.check(self.__player, self.__obstacle_group):
            fg_collision_sound.play()
            self.__fg_gameover = True
            self.__player.set_dead()
            #player é setado como morto se colidir com obstáculo

    def render(self):
        """Função que renderiza o jogo
        """
        screen.fill((0, 0, 0))

        self.__background.draw_background(screen)
        Score.draw_score(screen, self.__score.get_score())

        if self.__player._visible:
            self.__player_group.draw(screen)

        self.__obstacle_group.draw(screen)

        if self.__fg_gameover:
            screen.blit(death_box, (0, 0))
            # aparece a tela de gameover

        pygame.display.update()

        while self.__fg_gameover:
            self.__clock.tick(100)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__fg_gameover = False

                if event.type == KEYDOWN:
                    if event.key == K_y:
                        self.reset_game()

                    elif event.key == K_n:
                        pygame.quit()
                        quit()
                #teclas para reiniciar e sair do jogo

    def reset_game(self):
        """Função que define aspectos do jogo ao ser resetado
        """
        # resetando as configurações para recomeçar o jogo
        self.__fg_gameover = False
        self.__score._fg_speed = 2
        self.__score._fg_score = 0
        self.__obstacle_group.empty()
        self.__player.rect.center = [fg_player_x, fg_player_y]
        self.__player._visible = True
        self.__player.set_alive()

    pygame.display.set_caption('A Frog Journey')

if __name__ == "__main__":
    game = FrogJourneyGame()
    game.run()