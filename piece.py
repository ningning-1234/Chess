import pygame.sprite
from settings import *
from utils import *

pawn_white = pygame.image.load('assets/Pawn_W.png')
pawn_black = pygame.image.load('assets/Pawn_B.png')

king_white = pygame.image.load('assets/King_W.png')
king_black = pygame.image.load('assets/King_B.png')

queen_white = pygame.image.load('assets/Queen_W.png')
queen_black = pygame.image.load('assets/Queen_B.png')

bishop_white = pygame.image.load('assets/Bishop_W.png')
bishop_black = pygame.image.load('assets/Bishop_B.png')

knight_white = pygame.image.load('assets/Knight_W.png')
knight_black = pygame.image.load('assets/Knight_B.png')

rook_white = pygame.image.load('assets/Rook_W.png')
rook_black = pygame.image.load('assets/Rook_B.png')

class Piece(pygame.sprite.Sprite):
    def __init__(self, grid_pos, player, name):
        super().__init__()
        self.game = None
        self.image = pawn_white
        self.rect = self.image.get_rect()
        self.grid_pos = grid_pos
        self.player = player
        self.name = name
        if (player == 1):
            self.name+=' w'
        if (player == 2):
            self.name+=' b'
        print(self)

    def __str__(self):
        return self.name + ' at ' + str(self.grid_pos)

    def captured(self, piece):
        print('captured by ' + str(piece))

    def get_moves(self):
        return []

    def highlight_moves(self):
        move_lst = self.get_moves()
        for pos in move_lst:
            if(get_tile(pos, self.game.tile_lst) is not None):
                if(get_tile(pos, self.game.tile_lst).piece is None):
                    self.game.tile_lst[pos[0]][pos[1]].color = HIGH_LIGHT_COLOR
                elif (get_tile(pos, self.game.tile_lst).piece.player != self.player):
                    self.game.tile_lst[pos[0]][pos[1]].color = (200, 0, 0)
                self.game.highlighted_tiles.append(self.game.tile_lst[pos[0]][pos[1]])

    def update(self):
        self.rect.topleft = (self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE)

    def draw(self, surface):
        pass

class Pawn(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'pawn')
        if (player == 1):
            self.image = pawn_white
        if (player == 2):
            self.image = pawn_black

class King(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'king')
        if (player == 1):
            self.image = king_white
        if (player == 2):
            self.image = king_black

    def get_moves(self):
        move_lst = []
        pos1 = (self.grid_pos[0] - 1, self.grid_pos[1] - 1)
        pos2 = (self.grid_pos[0], self.grid_pos[1] - 1)
        pos3 = (self.grid_pos[0] + 1, self.grid_pos[1] - 1)
        pos4 = (self.grid_pos[0] + 1, self.grid_pos[1])
        pos5 = (self.grid_pos[0] + 1, self.grid_pos[1] + 1)
        pos6 = (self.grid_pos[0], self.grid_pos[1] + 1)
        pos7 = (self.grid_pos[0] - 1, self.grid_pos[1] + 1)
        pos8 = (self.grid_pos[0] - 1, self.grid_pos[1])
        move_lst.append(pos1)
        move_lst.append(pos2)
        move_lst.append(pos3)
        move_lst.append(pos4)
        move_lst.append(pos5)
        move_lst.append(pos6)
        move_lst.append(pos7)
        move_lst.append(pos8)
        return move_lst

class Queen(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'queen')
        if (player == 1):
            self.image = queen_white
        if (player == 2):
            self.image = queen_black

    def get_moves(self):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1])
            move_lst.append(pos)
            if(get_tile(pos, self.game.tile_lst) is None):
                break
            elif(get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1])
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0], self.grid_pos[1] - tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0], self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1] - tile)
            move_lst.append(pos)
            if(get_tile(pos, self.game.tile_lst) is None):
                break
            elif(get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1] - tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        return move_lst

class Bishop(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'bishop')
        if (player == 1):
            self.image = bishop_white
        if (player == 2):
            self.image = bishop_black

    def get_moves(self):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1] - tile)
            move_lst.append(pos)
            if(get_tile(pos, self.game.tile_lst) is None):
                break
            elif(get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1] - tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        return move_lst

class Knight(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'knight')
        if(player == 1):
            self.image = knight_white
        if(player == 2):
            self.image = knight_black

    def get_moves(self):
        move_lst = []
        pos1 = (self.grid_pos[0] - 1, self.grid_pos[1] - 2)
        pos2 = (self.grid_pos[0] + 1, self.grid_pos[1] - 2)
        pos3 = (self.grid_pos[0] + 2, self.grid_pos[1] - 1)
        pos4 = (self.grid_pos[0] + 2, self.grid_pos[1] + 1)
        pos5 = (self.grid_pos[0] + 1, self.grid_pos[1] + 2)
        pos6 = (self.grid_pos[0] - 1, self.grid_pos[1] + 2)
        pos7 = (self.grid_pos[0] - 2, self.grid_pos[1] + 1)
        pos8 = (self.grid_pos[0] - 2, self.grid_pos[1] - 1)
        move_lst.append(pos1)
        move_lst.append(pos2)
        move_lst.append(pos3)
        move_lst.append(pos4)
        move_lst.append(pos5)
        move_lst.append(pos6)
        move_lst.append(pos7)
        move_lst.append(pos8)
        return move_lst

class Rook(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'rook')
        if (player == 1):
            self.image = rook_white
        if (player == 2):
            self.image = rook_black

    def get_moves(self):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1])
            move_lst.append(pos)
            if(get_tile(pos, self.game.tile_lst) is None):
                break
            elif(get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0] + tile, self.grid_pos[1])
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0], self.grid_pos[1] - tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        for tile in range(1, 8):
            pos = (self.grid_pos[0], self.grid_pos[1] + tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
                break
        return move_lst
