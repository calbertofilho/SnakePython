import pygame
from pygame.locals import *

class Handycap(pygame.sprite.Sprite):
    '''Classe que representa o obstáculo no cenário'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.length = 0
    def update(self):
        '''Método que representa o comportamento do obstáculo a cada iteração do jogo'''
    def set_position(self, pos_x, pos_y):
        '''Método que posiciona o obstáculo no cenário'''
        self.rect.x = pos_x
        self.rect.y = pos_y
    def get_position(self):
        '''Método que retorna a posição do obstáculo no cenário'''
        return self.rect
    def get_direction(self):
        '''Método que retorna a direção do obstáculo no cenário'''
        return self.direction
    def get_length(self):
        '''Método que retorna o comprimento do obstáculo no cenário'''
        return self.length
