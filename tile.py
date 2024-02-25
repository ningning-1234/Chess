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
        self.piece_counter = []
        self.piece = None
        self.hover = False
        self.clicked = False

        self.bg_color = None
        self.border_color = None
        self.text = None

        # print(self.rect)
        #self.rect = pygame.Rect(grid_pos[0]*TILE_SIZE, grid_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def __str__(self):
        return str(self.grid_pos)

    def onclick(self, game):
        print(str(self)+' '+ str(self.piece) +' '+str(self.piece_counter))
        moved_piece = False
        #clicking on same tile
        if (game.clicked == self):
            # deselect current clicked tile
            self.clicked = False
            game.clicked = None
            for tile in game.highlighted_tiles:
                tile.color = tile.default_color
                tile.text = None
            game.highlighted_tiles = []
        else:
            # clicking on different tile
            if (game.clicked is not None):
                # movement
                if(game.clicked.piece is not None):
                    if (self.grid_pos in game.clicked.piece.move_lst and
                        game.current_turn == game.clicked.piece.player and
                        game.promoted is None):
                        #move to new tile
                        print(self.grid_pos)
                        game.clicked.piece.move(self.grid_pos)
                        moved_piece = True
                # deselect
                game.clicked.clicked = False
                game.clicked = None
                for tile in game.highlighted_tiles:
                    tile.color = tile.default_color
                    tile.text = None
                game.highlighted_tiles = []

            #clicking on a piece
            if(not moved_piece):
                game.clicked = self
                game.clicked.clicked = True
                if (game.clicked.piece is not None):
                    game.clicked.piece.highlight_moves()

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
        if(self.text is not None):
            self.image.blit(self.text, (0, 0))
