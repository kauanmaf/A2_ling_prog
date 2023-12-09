import pygame
import random
from settings import *
from abstract import *
from classes_base_flappy import *

class FlappyBird(Minigame_abs):
    """
    Classe representando o jogo Flappy Bird.

    Atributos:
    -----------
    - ``__screen`` (pygame.Surface):
        A superfície da tela do jogo.

    - ``__scroll_speed`` (int):
        A velocidade de rolagem do jogo.

    - ``__bird_position`` (tuple):
        A posição inicial do pássaro.

    - ``__bird`` (pygame.sprite.GroupSingle):
        O grupo de sprites contendo o pássaro.

    - ``__pipes`` (pygame.sprite.Group):
        O grupo de sprites contendo os canos.

    - ``__ground`` (pygame.sprite.Group):
        O grupo de sprites contendo os elementos do chão.

    - ``__collision_detector`` (CollisionDetector):
        Uma instância da classe CollisionDetector para lidar com colisões.

    - ``__score`` (int):
        A pontuação do jogador.

    - ``__pipe_timer`` (int):
        Um temporizador para controlar os intervalos de criação de canos.

    - ``__menu`` (Menu):
        Uma instância da classe Menu para exibir o menu do jogo.

    - ``__game_started`` (bool):
        Indica se o jogo foi iniciado.

    Métodos:
    --------
    - ``__init__(self, screen)``:
        Inicializa as variáveis necessárias para a criação do jogo.

    - ``create_bird(self)``:
        Cria um novo pássaro e o adiciona ao grupo de sprites do pássaro.

    - ``create_ground(self, x_pos_ground=0, y_pos_ground=530)``:
        Cria um novo grupo de sprites de chão com posições especificadas.

    - ``spawn_pipes(self, x_top=1300, x_bottom=1300)``:
        Cria canos em posições específicas com base em um temporizador.

    - ``update_score(self)``:
        Atualiza a pontuação do jogador com base nos canos passados.

    - ``reset_game(self)``:
        Reseta o estado do jogo para um novo jogo.

    - ``draw(self)``:
        Desenha os elementos do jogo na tela.

    - ``update(self)``:
        Atualiza o estado do jogo com base na entrada do usuário e colisões.

    - ``run(self)``:
        Executa o loop do jogo, lidando com início, reinício, desenho e atualização do jogo.
    """

    def __init__(self, screen):
        """
        Inicializa as variáveis necessárias para a criação do jogo
        """
        super().__init__()
        # Como todas as variáveis serão utilizadas apenas dentro dessa classe, podemos utiliza-las como atributos protegidos
        self.__screen = screen

        self.__score = 0
        self.pipe_timer = 100
        self.scroll_speed = 3
        self.bird_position = (200, screen_height / 2 -100)

        self.__menu = Menu(self.__screen, self.__bird_position)
        self.__game_started = False

        self.__bird = pygame.sprite.GroupSingle()
        self.__pipes = pygame.sprite.Group()
        self.__ground = self.create_ground()
        self.create_bird()

        self.__collision_detector = CollisionDetector(self.__bird, self.__ground, self.__pipes, self.__screen)

    @property
    def scroll_speed(self):
        """
        Obtém a velocidade de rolagem do jogo.

        Returns:
            int: A velocidade de rolagem do jogo.
        """
        return self.__scroll_speed
    
    @scroll_speed.setter
    def scroll_speed(self, scroll_speed_: int):
        """
        Define a velocidade de rolagem do jogo.

        Args:
            scroll_speed_ (int): A nova velocidade de rolagem do jogo.
        """
        self.__scroll_speed = scroll_speed_

    @property
    def pipe_timer(self):
        """
        Obtém o temporizador de geração de canos.

        Returns:
            int: O temporizador de geração de canos.
        """
        return self.__pipe_timer
    
    @pipe_timer.setter
    def pipe_timer(self, pipe_timer_: int):
        """
        Define o temporizador de geração de canos.

        Args:
            pipe_timer_ (int): O novo valor do temporizador de geração de canos.
        """
        self.__pipe_timer = pipe_timer_

    @property
    def bird_position(self):
        """
        Obtém a posição inicial do pássaro.

        Returns:
            tuple: As coordenadas da posição inicial do pássaro.
        """
        return self.__bird_position
    
    @bird_position.setter
    def bird_position(self, bird_position_: tuple):
        """
        Define a posição inicial do pássaro.

        Args:
            bird_position_ (tuple): As novas coordenadas da posição inicial do pássaro.
        """
        self.__bird_position = bird_position_


    def create_bird(self):
        """
        Cria um novo pássaro e o adiciona ao grupo de sprites do pássaro.
        """
        self.__bird.add(Bird(self.__bird_position))

    def create_ground(self, x_pos_ground = 0, y_pos_ground = 530):
        """
        Cria um novo grupo de sprites de chão com posições especificadas.

        """
        ground_group = pygame.sprite.Group()  # Create a group to hold grounds
        ground_group.add(Ground(x_pos_ground, y_pos_ground, self.__scroll_speed))
        ground_group.add(Ground(x_pos_ground + ground_image_flappy.get_width(), y_pos_ground, self.__scroll_speed))
        ground_group.add(Ground(x_pos_ground + 2 * ground_image_flappy.get_width(), y_pos_ground, self.__scroll_speed))
        return ground_group  

    def spawn_pipes(self, x_top = 1300, x_bottom = 1300):
        """
        Cria canos em posições específicas com base em um temporizador.
        """
        if len(self.__pipes) <= 0:
            self.pipe_timer = -1
        if self.__pipe_timer <= 0 and self.__bird.sprite._alive:

            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image_flappy.get_height()

            self.__pipes.add(Pipe(x_top, y_top, top_pipe_image_flappy, "top", self.__scroll_speed))
            self.__pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image_flappy, "bottom", self.__scroll_speed))

            self.pipe_timer = 100

        self.pipe_timer -= 1

    def update_score(self):
        """
        Atualiza a pontuação do jogador com base nos canos passados.
        """
        for pipe in self.__pipes.sprites():
            if not pipe._passed and pipe._pipe_type == "bottom":
                bird_rect = self.__bird.sprite.rect
                pipe_rect = pipe.rect
                exit_position = pipe_rect.x + pipe_rect.width

                if bird_rect.x > exit_position:
                    score_sound_flappy.play()
                    pipe._passed = True
                    self.__score += 1

    def reset_game(self):
        """
        Reseta o estado do jogo para um novo jogo.
        """
        # Setamos todas as variáveis para as variáveis iniciais
        self.__bird_position = (200, screen_height / 2 - 100)
        self.create_bird()
        self.__pipes.empty()
        self.__ground.empty()
        self.__ground = self.create_ground()
        self.__score = 0
        self.__pipe_timer = 100
        self.game_over = False
        self.__bird.sprite._alive = True 

        self.__collision_detector = CollisionDetector(self.__bird, self.__ground, self.__pipes, self.__screen)

    def draw(self):
        """
        Desenha os elementos do jogo na tela.
        """

        # Desenhando a imgaem de fundo
        self.__screen.blit(skyline_image_flappy, (0, 0))

        # Desenhando os canos
        self.__pipes.draw(self.__screen)

        # Desenhando o chão
        self.__ground.draw(self.__screen)

        # Desenhando o pássaro
        self.__bird.draw(self.__screen)

        # Spawning pipes
        self.spawn_pipes()

        # Desenhando a pontuação
        score_text = pygame.font.Font(None, 36).render(f"Score: {self.__score}", True, pygame.Color(255, 255, 255))
        self.__screen.blit(score_text, (20, 20))

    def update(self):
        """
        Atualiza o estado do jogo com base na entrada do usuário e colisões.
        """
        user_input = pygame.key.get_pressed()

        # Se a quantidade de grounds for menor ou igual a 2, adicionarmos uma imagem do chão.
        if len(self.__ground) <= 2:
            self.__ground = self.create_ground()

        # Se o pássaro estiver vivo, atualizamos o score, a criação de canos e a criação do chão
        if self.__bird.sprite._alive:
            self.update_score()
            self.__pipes.update()
            self.__ground.update()

        self.__bird.update(user_input)

        # Checando se há colisões entre o pássaro e outros elementos
        self.__collision_detector.check_collisions()
    
    def run(self):
        """
        Executa o loop do jogo, lidando com início, reinício, desenho e atualização do jogo.
        """
        keys = pygame.key.get_pressed()

        # Caso o jogo não tenha começado, desenhamos o menu
        if not self.__game_started:
            self.__menu.draw()
            if keys[pygame.K_SPACE]:
                transition_sound_flappy.play()
                self.__game_started = True
        
        # Se o passaro não estiver vivo e a tecla R é pressionada, o jogo é restaurado
        elif not self.__bird.sprite._alive and keys[pygame.K_r] :
            self.reset_game()

        # Pra outra situação, seguimos o jogo normalmente
        else:
            self.draw()
            self.update()
