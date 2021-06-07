from libs.settings import (
    SNAKE, BLOCKS
)
import pygame
from pygame.locals import *

class Snake(pygame.sprite.Sprite):
    '''Classe que representa a cobra'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = SNAKE[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.my_direction = 'Stop'
        self.body = [(0, 0), (0, BLOCKS), (0, (2 * BLOCKS))]
    def update(self):
        '''Método que representa o comportamento da cobra a cada iteração do jogo'''
    def set_initial_position(self, position):
        '''Método que seta a posição inicial da cobra na tela'''
        self.rect = position
    def set_direction(self, direction):
        '''Método que seta a direção da cabeça da cobra'''
        self.my_direction = direction
    def get_direction(self):
        '''Método que retorna a direção da cabeça da cobra'''
        return self.my_direction
    def grow_up(self):
        '''Método que cresce a cobra'''
        self.body.append((0, 0))
