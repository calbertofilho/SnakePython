'''
Jogo da Cobrinha em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 25/05/2021
'''
# pylint: disable=no-member
# pylint: disable=no-name-in-module

import os
import random
import sys
import pygame
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE,
    #K_PAUSE, K_UP, K_DOWN, K_LEFT, K_RIGHT
)
#from pygame.locals import *

# Constantes
BASE_DIR = os.path.dirname(__file__)                                  # Diretorio do jogo
VERSION = 'v1.0'                                                      # Versão do jogo
FPS = 15                                                              # Frames por segundo

class Screen():
    '''Classe que representa a tela do jogo'''
    def __init__(self):
        self.width = 800                                              # Comprimento da janela
        self.height = 600                                             # Altura da janela
        self.caption = f'SnakePython {VERSION}'                       # Título
        self.icon_location = f'{BASE_DIR}/assets/icons/icon.png'      # Local do ícone
        self.surface = pygame.display.set_mode((self.width, self.height)) # Criação da tela
        pygame.display.set_caption(self.caption)                      # Configuração do título
        self.icon = pygame.image.load(self.icon_location).convert_alpha() # Criação do ícone
        pygame.display.set_icon(self.icon)                            # Configuração do ícone
        os.environ['SDL_VIDEO_CENTERED'] = '1'                        # Centralização no desktop

    def update(self):
        '''Método que modela o comportamento da janela'''
        for event in pygame.event.get():                              # Controle de eventos
            if event.type == QUIT:                                    # Evento: Fechar a janela
                close_game()
            if event.type == KEYDOWN:                                 # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                             # Teste se a tecla é "ESC"
                    close_game()
        pygame.display.update()                                       # Atualização de tela

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

def init_libs():
    '''Função que inicializa as biliotecas utilizadas no jogo'''
    pygame.init()                                                     # Inicialização do PyGame
    pygame.mixer.pre_init(                                            # Inicialização do áudio
        frequency = 44100, size = 16, channels = 1, buffer = 512
    )

def create_level(sface, stage):
    '''Função que gera os mapas dos níveis do jogo'''
    panel = sface.get_surface()                                       # Painel de exibição do jogo
    panel.fill((0, 0, 0))                                             # Desenha uma tela preta
    if stage == 0:                                                    # Define a Tela de início
        blocks = 20
        size_x = sface.get_size()[0] // blocks
        size_y = sface.get_size()[1] // blocks
        for j in range(size_y):
            if (size_y - (blocks // 10)) > j >= (blocks // 10):
                for i in range(size_x):
                    if (size_x - (blocks // 10)) > i >= (blocks // 10):
                        pygame.draw.rect(
                            panel,
                            (255, 0, 0),
                            (i * blocks, j * blocks, blocks, blocks),
                            random.randint(0, 50) // 50
                        )

def close_game():
    '''Função que encerra o jogo'''
    pygame.quit()
    sys.exit()

def main():
    '''Função principal que contempla a lógica de execução do jogo'''
    init_libs()                                                       # Inicialização dos recursos
    screen = Screen()                                                 # Criação da janela
    sound_type = 'wav' if 'win' in sys.platform else 'ogg'            # Decisão do tipo de áudio
    clock = pygame.time.Clock()                                       # Controle de tempo do jogo
    level = 0                                                         # Configura pra tela de início
    create_level(screen, level)                                       # Cria a tela selecionada
    start = True                                                      # Dá início a execução do jogo

    while start:
        clock.tick(FPS)
        screen.update()

try:
    while True:
        main()
except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")
finally:
    close_game()
