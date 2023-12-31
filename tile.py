import pygame
from piece import *
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_pos):
        super(Tile, self).__init__()
        self.grid_pos = grid_pos
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        if ((grid_pos[0] + grid_pos[1]) % 2 != 1):
            self.color = BOARD_COLOR_1
        else:
            self.color = BOARD_COLOR_2
        self.default_color = self.color
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = TILE_SIZE * grid_pos[0]
        self.rect.y = TILE_SIZE * grid_pos[1]
        self.piece = None
        self.hover = False
        self.clicked = False

        self.bg_color = None
        self.border_color = None

        # print(self.rect)
        #self.rect = pygame.Rect(grid_pos[0]*TILE_SIZE, grid_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def onclick(self):
        print('clicked')

    def update(self):
        if(self.hover):
            self.bg_color = (
                max(self.color[0]-50, 0),
                max(self.color[1]-50, 0),
                max(self.color[2]-50, 0)
            )
        else:
            self.bg_color = None

        if(self.clicked):
            self.border_color = ((200, 0, 0), 4)
        else:
            self.border_color = None
        self.draw()

    def draw(self):
        if(self.bg_color is not None):
            self.image.fill(self.bg_color)
        else:
            self.image.fill(self.color)

        if (self.border_color is not None):
            pygame.draw.rect(self.image, self.border_color[0], (0, 0, TILE_SIZE, TILE_SIZE), self.border_color[1])
        else:
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)

