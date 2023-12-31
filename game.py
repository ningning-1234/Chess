import pygame
from tile import *
from settings import *
from utils import *

def generate_pieces(game):
    # Generate pieces
    # for pawn in range(0, 8):
    #     pawn_w = Pawn((pawn, 6), 1)
    #     game.add_piece(pawn_w)
    # for pawn in range(0, 8):
    #     pawn_b = Pawn((pawn, 1), 2)
    #     game.add_piece(pawn_b)

    king_w = King((4, 6), 1)
    game.add_piece(king_w)
    king_b = King((4, 0), 2)
    game.add_piece(king_b)

    queen_w = Queen((3, 7), 1)
    game.add_piece(queen_w)
    queen_b = Queen((3, 0), 2)
    game.add_piece(queen_b)

    bishop1_w = Bishop((2, 7), 1)
    game.add_piece(bishop1_w)
    bishop2_w = Bishop((5, 7), 1)
    game.add_piece(bishop2_w)
    bishop1_b = Bishop((2, 0), 2)
    game.add_piece(bishop1_b)
    bishop2_b = Bishop((5, 0), 2)
    game.add_piece(bishop2_b)

    knight1_w = Knight((1, 7), 1)
    game.add_piece(knight1_w)
    knight2_w = Knight((6, 7), 1)
    game.add_piece(knight2_w)
    knight1_b = Knight((1, 0), 2)
    game.add_piece(knight1_b)
    knight2_b = Knight((6, 0), 2)
    game.add_piece(knight2_b)

    rook1_w = Rook((0, 2), 1)
    game.add_piece(rook1_w)
    rook2_w = Rook((7, 7), 1)
    game.add_piece(rook2_w)
    rook1_b = Rook((0, 0), 2)
    game.add_piece(rook1_b)
    rook2_b = Rook((7, 0), 2)
    game.add_piece(rook2_b)

class ChessGame():
    def __init__(self):
        self.turn_count = 1
        self.taken_pieces = []
        self.tile_lst = []
        self.tile_group = pygame.sprite.Group()
        self.piece_lst = []
        self.piece_group = pygame.sprite.Group()

        self.board_pos = (60,60)
        self.board_surface = pygame.surface.Surface((TILE_SIZE*8, TILE_SIZE*8))
        self.highlighted_tiles = []
        self.clicked = None

    def add_piece(self, piece):
        self.piece_lst.append(piece)
        self.piece_group.add(piece)
        piece.game = self
        self.tile_lst[piece.grid_pos[0]][piece.grid_pos[1]].piece = piece

    def generate_board(self):
        # Generate grid
        for tiles_x in range(GRID_SIZE):
            self.tile_lst.append([])
            for tiles_y in range(GRID_SIZE):
                t = Tile((tiles_x, tiles_y))
                self.tile_lst[tiles_x].append(t)
                self.tile_group.add(t)
        generate_pieces(self)

    def update(self, events, mouse_events):
        mouse_pos = (mouse_events['pos'][0] - self.board_pos[0], mouse_events['pos'][1] - self.board_pos[1])
        hovered = None
        for tile_x in self.tile_lst:
            for tile_y in tile_x:
                tile_y.hover = False
                if(between_nums(tile_y.rect.left, tile_y.rect.right, mouse_pos[0])):
                    if (between_nums(tile_y.rect.top, tile_y.rect.bottom, mouse_pos[1])):
                        tile_y.hover = True
                        hovered = tile_y
        for event in events:
            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button==1):
                    if (hovered is not None):
                        if (self.clicked == hovered):
                            #deselect current clicked tile
                            self.clicked.clicked = False
                            self.clicked = None
                            for tile in self.highlighted_tiles:
                                tile.color = tile.default_color
                            self.highlighted_tiles = []
                        else:
                            # deselect current clicked tile
                            if (self.clicked is not None):
                                self.clicked.clicked = False
                                self.clicked = None
                                for tile in self.highlighted_tiles:
                                    tile.color = tile.default_color
                                self.highlighted_tiles = []

                            self.clicked = hovered
                            self.clicked.clicked = True
                            self.clicked.onclick()
                            if (self.clicked.piece is not None):
                                self.clicked.piece.highlight_moves()

        self.tile_group.update()
        self.piece_group.update()

    def draw(self, surface):
        self.tile_group.draw(self.board_surface)
        self.piece_group.draw(self.board_surface)
        surface.blit(self.board_surface,self.board_pos)
