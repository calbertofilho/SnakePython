import os
from libs.functions import (
    close_game, pause_game
)
from libs.settings import (
    VERSION, BASE_DIR
)
import pygame
from pygame.constants import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_PAUSE,
)
from pygame.locals import *

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
                if event.key == K_ESCAPE:                            # Testa se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_PAUSE:                             # Testa se a tecla é "PAUSE"
                    pause_game(self, True)                           # Chamada da função de pausar
        pygame.display.update()                                      # Atualização de tela
    def get_surface(self):
        '''Método que retorna o painel de exibição dos objetos da janela'''
        return self.surface
    def get_size(self):
        '''Método que retorna o tamanho da tela'''
        return (self.width, self.height)
