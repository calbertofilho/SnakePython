'''
Jogo da Cobrinha em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 31/05/2021
'''
# pylint: disable=no-member
# pylint: disable=no-name-in-module

import os
import random
import sys
import time
import pygame
from pygame.constants import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_SPACE, K_PAUSE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT
)
#from pygame.locals import *

# Constantes
BASE_DIR = os.path.dirname(__file__)                                 # Diretorio do jogo
VERSION = 'v1.0'                                                     # Versão do jogo
FPS = 15                                                             # Frames por segundo
BLOCKS = 20                                                          # Tamanho do bloco da matriz
TILES = BLOCKS * 2                                                   # Tamanho das imagens tiles
SCALE = (TILES, TILES)                                               # Escala criação dos TileMaps
# Ativos
SCENERY = None                                                       # TileMap do cenário
SNAKE = None                                                         # TileMap da cobra
RABBIT = None                                                        # Frames da animação do coelho
BGM = None                                                           # Músicas de fundo
FX = None                                                            # Efeitos
MAP = []                                                             # Mapa dos objetos da fase
# Definições de áudio
VOLUME_FX = 0.3                                                      # Volume dos efeitos especiais
VOLUME_BGM = 0.6                                                     # Volume da música de fundo
FADEOUT_BGM = 1500                                                   # Fade pra parar a música

class Screen():
    '''Classe que representa a tela do jogo'''
    def __init__(self):
        self.width = 800                                             # Comprimento da janela
        self.height = 600                                            # Altura da janela
        self.caption = f'SnakePython {VERSION}'                      # Título
        self.icon_location = f'{BASE_DIR}/assets/icons/icon.png'     # Local do ícone
        self.surface = pygame.display.set_mode((self.width, self.height)) # Criação da tela
        pygame.display.set_caption(self.caption)                     # Configuração do título
        self.icon = pygame.image.load(self.icon_location).convert_alpha() # Criação do ícone
        pygame.display.set_icon(self.icon)                           # Configuração do ícone
        os.environ['SDL_VIDEO_CENTERED'] = '1'                       # Centralização no desktop
    def update(self):
        '''Método que modela o comportamento da janela'''
        for event in pygame.event.get():                             # Identifica os eventos
            if event.type == QUIT:                                   # Evento: Fechar a janela
                close_game()                                         # Chamada da função de fechar
            if event.type == KEYDOWN:                                # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                            # Teste se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_PAUSE:                             # Teste se a tecla é "PAUSE"
                    pause_game(self, True)                           # Chamada da função de pausar
                if event.key == K_SPACE:
                    level = random.randint(1, 5)
                    create_level(self, level)
        pygame.display.update()                                      # Atualização de tela
    def get_surface(self):
        '''Método que retorna o painel de exibição dos objetos da janela'''
        return self.surface
    def get_size(self):
        '''Método que retorna o tamanho da tela'''
        return (self.width, self.height)

class Snake(pygame.sprite.Sprite):
    '''Classe que representa a cobra'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.my_direction = 'Left'
    def update(self):
        '''Método que representa o comportamento da cobra a cada iteração do jogo'''
    def get_direction(self):
        '''Método que retorna a direção da cabeça da cobra'''

class Rabbit(pygame.sprite.Sprite):
    '''Classe que representa o coelho'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        '''Método que representa o comportamento do coelho a cada iteração do jogo'''

def init_libs(quality):
    '''Função que inicializa as biliotecas utilizadas no jogo'''
    if quality == 'high':                                            # Decisão da qualidade de som
        buf = 2048                                                   # Alta qualidade
    elif quality == 'mid':
        buf = 1024                                                   # Qualidade média
    else:
        buf = 512                                                    # Qualidade baixa
    pygame.init()                                                    # Inicialização do PyGame
    pygame.mixer.pre_init(                                           # Inicialização do áudio
        frequency = 44100,                                           # Frequência de 44100MHz
        size = -16,                                                  # Comprimento de onda 16bits
        channels = 2,                                                # Tocar em Stereo, 2 canais
        buffer = buf                                                 # Qualidade do som
    )

def populate_assets():
    '''Função que inicializa todos os ativos utilizados no jogo'''
    global SCENERY, SNAKE, RABBIT, BGM, FX                           # Indica alteração na variável global
    SCENERY = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/border.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/corner.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/incorner.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/ground.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/void.png'), SCALE)
    )
    SNAKE = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/head.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/body.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/curve.png'), SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/tail.png'), SCALE)
    )
    RABBIT = (
        # Carregar os frames da animação do coelho aqui
    )
    BGM = (
        f'{BASE_DIR}/assets/sounds/bgm/main.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level1.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level2.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level3.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level4.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level5.mid'
    )
    sound_type = 'wav' if 'win' in sys.platform else 'ogg'           # Decisão do tipo de áudio
    FX = (
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/eat.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/die.{sound_type}')
    )

def wait(delay):
    '''Função que atrasa a execução do código por um tempo determinado em segundos'''
    time_to_delay = time.time() + delay                              # Tempo inicial mais o delay
    while time.time() <= time_to_delay:                              # Enquanto não passar o delay
        None                                                         # Não faz nada


def play_bgm(track):
    '''Função para executar a música de fundo do jogo'''
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(BGM[track])                          # Carrega a música pra executar
        pygame.mixer.music.set_volume(VOLUME_BGM)                    # Configura o volume
        pygame.mixer.music.play(loops = -1)                          # Executa a música em loop

def pause_bgm(state):
    '''Função para suspender e resumir a música de fundo do jogo'''
    if pygame.mixer.music.get_busy():                                # Testa se há algo tocando
        if state is True:                                            # Se recebeu o valor True
            pygame.mixer.music.pause()                               # Pausa a execução
    else:                                                            # Se não há playback
        if state is False:                                           # Se recebeu o valor False
            pygame.mixer.music.unpause()                             # Retorna a execução

def stop_bgm(delay):
    '''Função para para a música de fundo do jogo'''
    pygame.mixer.music.fadeout(delay)                                # Executa o fadeout da música
    wait(delay / 1000)                                               # Transforma em segundos e espera
    pygame.mixer.music.stop()                                        # Para a execução da música

def get_scenery_tile(tilemap):
    '''Função que retorna as peças para a montagem do cenário'''
    scenery_tile = None
    if 'border' in tilemap:
        if 'out' in tilemap:
            if 'top' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[0], 0)
            if 'left' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[0], 90)
            if 'bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[0], 180)
            if 'right' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[0], 270)
        if 'in' in tilemap:
            if 'top' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 0)
            if 'left' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 90)
            if 'bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 180)
            if 'right' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 270)
    if 'corner' in tilemap:
        if 'out' in tilemap:
            if 'left_top' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[1], 0)
            if 'left_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[1], 90)
            if 'right_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[1], 180)
            if 'right_top' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[1], 270)
        if 'in' in tilemap:
            if 'left_top' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[2], 0)
            if 'left_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[2], 90)
            if 'right_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[2], 180)
            if 'right_top' in tilemap:
                scenery_tile = pygame.transform.rotate(SCENERY[2], 270)
    if 'ground' in tilemap:
        scenery_tile = pygame.transform.rotate(SCENERY[3], 0)
    if 'void' in tilemap:
        scenery_tile = pygame.transform.rotate(SCENERY[4], 0)
    return scenery_tile

def create_base_stage(sface):
    '''Função que gera o mapa mais básico do jogo'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    # Desenho do terreno
    size_x = sface.get_size()[0] // TILES                            # Tamanho de colunas da tela
    size_y = sface.get_size()[1] // TILES                            # Tamanho de linhas da tela
    for column in range(size_x):                                     # Para cada coluna
        for row in range(size_y):                                    # Para cada linha
            panel.blit(get_scenery_tile('ground'), (column * TILES, row * TILES)) # Representação do chão
    # Desenho das cantos                                             # Representação dos cantos
    panel.blit(get_scenery_tile('corner_out_left_top'), (0, 0))      # Externo superior esquerdo
    panel.blit(get_scenery_tile('corner_out_left_bottom'), (0, 560)) # Externo inferior esquerdo
    panel.blit(get_scenery_tile('corner_out_right_top'), (760, 0))   # Externo superior direito
    panel.blit(get_scenery_tile('corner_out_right_bottom'), (760, 560)) # Externo inferior direito
    for row in range(TILES, sface.get_size()[0] - TILES, TILES):     # Representação das bordas
        panel.blit(get_scenery_tile('border_out_top'), (row, 0))     # Externa superior
        panel.blit(get_scenery_tile('border_out_bottom'), (row, 560)) # Externa inferior
    for column in range(TILES, sface.get_size()[1] - TILES, TILES):  # Representação das laterais
        panel.blit(get_scenery_tile('border_out_left'), (0, column)) # Lateral externa esquerda
        panel.blit(get_scenery_tile('border_out_right'), (760, column)) # Lateral externa direita
    # Criação da matriz com o mapa de navegação dos obstáculos
    for row in range(size_y * 2):                                    # Representação do chão
        MAP.append([0] * (size_x * 2))                               # Preenchimento com zeros
    MAP[0][0] = 1                      # Representação dos cantos    # Externo superior esquerdo
    MAP[580 // BLOCKS][0] = 1                                        # Externo inferior esquerdo
    MAP[0][780 // BLOCKS] = 1                                        # Externo superior direito
    MAP[580 // BLOCKS][780 // BLOCKS] = 1                            # Externo inferior direito
    for row in range(BLOCKS, sface.get_size()[0] - BLOCKS, BLOCKS):  # Representação das bordas
        MAP[0][row // BLOCKS] = 1                                    # Externa superior
        MAP[580 // BLOCKS][row // BLOCKS] = 1                        # Externa inferior
    for column in range(BLOCKS, sface.get_size()[1] - BLOCKS, BLOCKS): # Representação das laterais
        MAP[column // BLOCKS][0] = 1                                 # Lateral externa esquerda
        MAP[column // BLOCKS][780 // BLOCKS] = 1                     # Lateral externa direita

def show_matrix(sface):
    '''Função que desenha na tela toda a matriz de obstáculos do jogo'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    size_x = sface.get_size()[0] // BLOCKS                           # Tamanho de colunas da matriz
    size_y = sface.get_size()[1] // BLOCKS                           # Tamanho de linhas da matriz
    for row in range(size_y):                                        # Para cada linha da matriz
        for column in range(size_x):                                 # Para cada coluna da matriz
            fill = 0 if MAP[row][column] == 1 else 1                 # Representa o preenchimento
            pygame.draw.rect(                                        # Desenha o retângulo na posição
                panel,                                               # Painel de exibição do jogo
                (255, 0, 0),                                         # Cor: Vermelha
                (column * BLOCKS, row * BLOCKS, BLOCKS, BLOCKS),     # Posição na tela
                fill                                                 # Tipo de preenchimento
            )

def create_obstacles(sface, num_obstacles):
    '''Função que gera os obstáculos da fase'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    # Criação dos obstáculos
    obstacles = []
    for qty in range(1, num_obstacles):
        size = random.randint(2, 10)
        direction = random.randint(0, 1)
        if direction == 0:
            position = (
                (random.randint(60, sface.get_size()[0] - 100 - (size * TILES)) // 10) * 10,
                (random.randint(60, sface.get_size()[1] - 100) // 10) * 10
            )
        if direction == 1:
            position = (
                (random.randint(60, sface.get_size()[0] - 100) // 10) * 10,
                (random.randint(60, sface.get_size()[1] - 100 - (size * TILES)) // 10) * 10
            )
        handicap = (position, size, direction)
        obstacles.insert(qty, handicap)
    print(num_obstacles - 1)
    # Desenho dos obstáculos
    for num, obstacle in enumerate(obstacles):
        position = obstacle[0]
        size = obstacle[1]
        direction = obstacle[2]
        if direction == 0:
            panel.blit(get_scenery_tile('corner_in_left_top'), position)
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (position[0], position[1] + TILES))
            for iterator in range(1, size + 1):
                panel.blit(get_scenery_tile('border_in_top'), (position[0] + (iterator * TILES), position[1]))
                panel.blit(get_scenery_tile('border_in_bottom'), (position[0] + (iterator * TILES), position[1] + TILES))
            panel.blit(get_scenery_tile('corner_in_right_top'), (position[0] + (iterator * TILES) + TILES, position[1]))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (position[0] + (iterator * TILES) + TILES, position[1] + TILES))
        if direction == 1:
            panel.blit(get_scenery_tile('corner_in_left_top'), position)
            panel.blit(get_scenery_tile('corner_in_right_top'), (position[0] + TILES, position[1]))
            for iterator in range(1, size + 1):
                panel.blit(get_scenery_tile('border_in_left'), (position[0], position[1] + (iterator * TILES)))
                panel.blit(get_scenery_tile('border_in_right'), (position[0] + TILES, position[1] + (iterator * TILES)))
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (position[0], position[1] + (iterator * TILES) + TILES))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (position[0] + TILES, position[1] + (iterator * TILES) + TILES))
        print(num, obstacle)
    # Adição dos obstáculos na matriz de navegação do jogo
    show_matrix(sface)                                               # Exibe a matriz na tela

def splash_screen(sface):
    '''Função que faz a animação da tela de abertura do jogo'''
    show_matrix(sface)                                               # Exibe a matriz na tela

def create_level(sface, stage):
    '''Função que gera os mapas dos níveis do jogo'''
    create_base_stage(sface)                                         # Cria o cenário básico
    play_bgm(stage)                                                  # Inicia a música de fundo
    if stage == 0:
        splash_screen(sface)                                         # Chama a tela de abertura
    else:
        create_obstacles(sface, (stage + 1))                         # Cria o nível

def pause_game(sface, state):
    pause_bgm(state)                                                 # Pausa a execução da música
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    while state:                                                     # Enquanto estiver pausado
        panel.fill((0, 0, 0))                                        # Exibe a mensagem de pause
        for event in pygame.event.get():                             # Identifica os eventos
            if event.type == QUIT:                                   # Evento: Fechar a janela
                close_game()                                         # Chamada da função de fechar
            if event.type == KEYDOWN:                                # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                            # Teste se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_PAUSE:                             # Teste se a tecla é "PAUSE"
                    state = False                                    # Altera o estado e sai de PAUSE
                    pause_bgm(state)                                 # Reinicia a execução da música
        sface.update()                                               # Atualização da tela

def close_game():
    '''Função que encerra o jogo'''
    pygame.quit()                                                    # Fecha a biblioteca PyGame
    pygame.mixer.quit()                                              # Encerra o reprodutor de aúdio
    sys.exit()                                                       # Encerra a execução

def main():
    '''Função principal que contempla a lógica de execução do jogo'''
    clock = pygame.time.Clock()                                      # Controle de tempo do jogo
    init_libs('low')                                                 # Inicialização dos recursos
    populate_assets()                                                # Carrega os ativos do jogo
    screen = Screen()                                                # Criação da janela
    snake = Snake()                                                  # Criação da cobra
    level = 0                                                        # Configura pra tela de início
    create_level(screen, level)                                      # Cria a tela selecionada
    start = True                                                     # Dá início a execução do jogo
    while start:                                                     # Enquanto estiver em execução
        clock.tick(FPS)                                              # Configura o FPS do jogo
        commands = pygame.key.get_pressed()                          # Armazena os comandos do jogo
        if commands[K_UP]:                                           # Se pressionar a seta pra cima
            snake.my_direction = 'Up'                                # Indica que a cobra vai para cima
        if commands[K_DOWN]:                                         # Se pressionar a seta pra baixo
            snake.my_direction = 'Down'                              # Indica que a cobra vai para baixo
        if commands[K_LEFT]:                                         # Se pressionar a seta da esquerda
            snake.my_direction = 'Left'                              # Indica que a cobra vai para esquerda
        if commands[K_RIGHT]:                                        # Se pressionar a seta da direita
            snake.my_direction = 'Right'                             # Indica que a cobra vai para direita
        screen.update()                                              # Atualiza a tela
        snake.update()                                               # Atualiza a cobra

try:                                                                 # Tenta executar
    while True:                                                      # Loop infinito
        main()                                                       # Dá início ao jogo
except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc: # Trata as exceções de erro
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")            # Feedback do que ocorreu
finally:                                                             # Finaliza
    close_game()                                                     # Chamada de saída do jogo
