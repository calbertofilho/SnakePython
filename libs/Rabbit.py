from libs.functions import (
    wait
)
from libs.settings import (
    RABBIT
)
import pygame
from pygame.locals import *

class Rabbit(pygame.sprite.Sprite):
    '''Classe que representa o coelho'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_image = 0
        self.image = RABBIT[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
    def update(self):
        '''Método que representa o comportamento do coelho a cada iteração do jogo'''
        self.current_image = (self.current_image + 1) % len(RABBIT)
        self.image = RABBIT[self.current_image]
        wait(0.1)
    def set_position(self, pos_x, pos_y):
        '''Método que posiciona o coelho na tela'''
        self.rect.x = pos_x
        self.rect.y = pos_y
    def get_position(self):
        '''Método que retorna a posição do coelho na tela'''
        return self.rect
