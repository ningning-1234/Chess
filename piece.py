import pygame.sprite
from settings import *
from utils import *

pawn_white = pygame.image.load('assets/Pawn_W.png')
pawn_black = pygame.image.load('assets/Pawn_B.png')

pawn_white_e = pygame.image.load('assets/Pawn_W_E.png')
pawn_black_e = pygame.image.load('assets/Pawn_B_E.png')

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

        self.move_lst = []

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

    def filter_moves(self, moves_temp):
        moves = []
        for tile in moves_temp:
            t = get_tile(tile, self.game.tile_lst)
            if(t is not None):
                if(t.piece is None or t.piece.player != self.player):
                    moves.append(tile)
                if(self.player != self.game.current_turn):
                    t.piece_counter.append(self)
        return moves

    def move(self, new_pos):
        self.game.tile_lst[self.grid_pos[0]][self.grid_pos[1]].piece = None
        self.grid_pos = new_pos
        new_tile = self.game.tile_lst[new_pos[0]][new_pos[1]]
        if(new_tile.piece is not None):
            #capture
            print('captured ' + str(new_tile.piece))
            if(new_tile.piece.player != self.player):
                if(self.player == 1):
                    self.game.captures_p1.append(new_tile.piece)
                    #self.game.white_piece_lst.remove(new_tile.piece)
                if (self.player == 2):
                    self.game.captures_p2.append(new_tile.piece)
                    #self.game.black_piece_lst.remove(new_tile.piece)
                self.game.piece_lst.remove(new_tile.piece)
                self.game.piece_group.remove(new_tile.piece)
        new_tile.piece = self
        self.game.change_turn()

    def highlight_moves(self):
        move_lst = self.move_lst
        for pos in move_lst:
            t = get_tile(pos, self.game.tile_lst)
            if(t.piece is None):
                if(self.game.current_turn == self.player and
                   self.game.promoted is None):
                    if(len(t.piece_counter) != 0):
                        # Displays how much opponent pieces are targeting that tile
                        t.color = OPPONENT_CAPTURE_COLOR
                        text_renderer = pygame.font.Font('freesansbold.ttf', 50)
                        text = text_renderer.render(str(len(t.piece_counter)), False, (0, 0, 0))
                        t.text = text
                    else:
                        # Displays if no pieces are targeting that tile
                        t.color = PLAYER_MOVE_COLOR
                else:
                    t.color = OPPONENT_MOVE_COLOR
            else:
                if (self.game.current_turn == self.player and
                   self.game.promoted is None):
                    t.color = PLAYER_CAPTURE_COLOR
                    if (len(t.piece_counter) != 0):
                        text_renderer = pygame.font.Font('freesansbold.ttf', 50)
                        text = text_renderer.render(str(len(t.piece_counter)), False, (0, 0, 0))
                        t.text = text
                else:
                    t.color = OPPONENT_CAPTURE_COLOR

            self.game.highlighted_tiles.append(self.game.tile_lst[pos[0]][pos[1]])

    def update(self):
        self.rect.topleft = (self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE)

    def draw(self, surface):
        pass

class Pawn(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'pawn')
        if (player == 1):
            self.image_default = pawn_white
            self.image_enp = pawn_white_e
            self.image = self.image_default
        if (player == 2):
            self.image_default = pawn_black
            self.image_enp = pawn_black_e
            self.image = self.image_default
        self.first_move = True
        self.en_passant = False
        self.en_passant_capture = None

    def get_moves(self):
        self.en_passant_capture = None
        move_lst = []
        if(self.player == 1):
            pos1 = (self.grid_pos[0], self.grid_pos[1] - 1)
            pos2 = (self.grid_pos[0], self.grid_pos[1] - 2)
            pos3 = (self.grid_pos[0] - 1, self.grid_pos[1] - 1)
            pos4 = (self.grid_pos[0] + 1, self.grid_pos[1] - 1)
            move_lst.append(pos1)
            move_lst.append(pos2)
            move_lst.append(pos3)
            move_lst.append(pos4)
        if (self.player == 2):
            pos1 = (self.grid_pos[0], self.grid_pos[1] + 1)
            pos2 = (self.grid_pos[0], self.grid_pos[1] + 2)
            pos3 = (self.grid_pos[0] - 1, self.grid_pos[1] + 1)
            pos4 = (self.grid_pos[0] + 1, self.grid_pos[1] + 1)
            move_lst.append(pos1)
            move_lst.append(pos2)
            move_lst.append(pos3)
            move_lst.append(pos4)
        self.move_lst = self.filter_moves(move_lst)
        #disable enpassant
        if(self.en_passant and self.player == self.game.current_turn):
            self.en_passant = False
        # self.en_passant_capture = False
        return self.move_lst

    def filter_moves(self, moves_temp):
        filtered_moves = []
        moves = []
        for tile in moves_temp:
            t = get_tile(tile, self.game.tile_lst)
            if (t is not None and (t.piece is None or t.piece.player != self.player)):
                filtered_moves.append(True)
            else:
                filtered_moves.append(False)
        # Move 1 tile
        if (filtered_moves[0] == True):
            if (get_tile(moves_temp[0], self.game.tile_lst).piece is None):
                moves.append(moves_temp[0])
                # Move 2 tiles
                if (filtered_moves[1] == True):
                    if (get_tile(moves_temp[1], self.game.tile_lst).piece is None):
                        if (self.first_move == True):
                            moves.append(moves_temp[1])
        # Capture left
        if (filtered_moves[2] == True):
            #movement
            if (get_tile(moves_temp[2], self.game.tile_lst).piece is not None):
                moves.append(moves_temp[2])
            # capture highlight
            if (self.player != self.game.current_turn):
                get_tile(moves_temp[2], self.game.tile_lst).piece_counter.append(self)
            # en_passant
            p = get_tile((self.grid_pos[0]-1, self.grid_pos[1]), self.game.tile_lst).piece
            if (p is not None and type(p)==Pawn):
                if (p.player!=self.player and p.en_passant):
                    moves.append(moves_temp[2])
                    self.en_passant_capture = p
                    if (self.player != self.game.current_turn):
                        get_tile(moves_temp[2], self.game.tile_lst).piece_counter.append(self)
        # Capture right
        if (filtered_moves[3] == True):
            if (get_tile(moves_temp[3], self.game.tile_lst).piece is not None):
                moves.append(moves_temp[3])
            if (self.player != self.game.current_turn):
                get_tile(moves_temp[3], self.game.tile_lst).piece_counter.append(self)
            # en_passant
            p = get_tile((self.grid_pos[0] + 1, self.grid_pos[1]), self.game.tile_lst).piece
            if (p is not None and type(p) == Pawn):
                if (p.player != self.player and p.en_passant):
                    moves.append(moves_temp[3])
                    self.en_passant_capture = p
                    if (self.player != self.game.current_turn):
                        get_tile(moves_temp[3], self.game.tile_lst).piece_counter.append(self)
        return moves

    def move(self, new_pos):
        self.game.tile_lst[self.grid_pos[0]][self.grid_pos[1]].piece = None
        #set enpassant if moving 2 squars
        if (new_pos[1] == self.grid_pos[1] - 2 or new_pos[1] == self.grid_pos[1] + 2):
            self.en_passant = True

        self.grid_pos = new_pos
        new_tile = self.game.tile_lst[new_pos[0]][new_pos[1]]
        self.first_move = False
        if(new_tile.piece is not None):
            #capture
            print('captured ' + str(new_tile.piece))
            if(new_tile.piece.player != self.player):
                if(self.player == 1):
                    self.game.captures_p1.append(new_tile.piece)
                if (self.player == 2):
                    self.game.captures_p2.append(new_tile.piece)
                self.game.piece_lst.remove(new_tile.piece)
                self.game.piece_group.remove(new_tile.piece)
        elif(self.en_passant_capture is not None):
            #piece to capture
            if (self.player == 1):
                p = get_tile((self.grid_pos[0], self.grid_pos[1] + 1), self.game.tile_lst).piece
                if(p==self.en_passant_capture):
                    self.game.captures_p1.append(p)
                    print('en passant')
                    self.game.piece_lst.remove(p)
                    self.game.piece_group.remove(p)
            else:
                p = get_tile((self.grid_pos[0], self.grid_pos[1] - 1), self.game.tile_lst).piece
                if (p == self.en_passant_capture):
                    self.game.captures_p2.append(p)
                    print('en passant')
                    self.game.piece_lst.remove(p)
                    self.game.piece_group.remove(p)
        self.en_passant_capture = None

        new_tile.piece = self
        if(self.grid_pos[1] == 0 or self.grid_pos[1] == 7):
            self.game.promoted = self
            for piece in self.game.piece_lst:
                piece.get_moves()
            # self.game.current_turn *=-1
            # self.promotion()

        if(self.game.promoted is None):
            self.game.change_turn()

    def promotion(self, piece='queen'):
        #remove pawn
        self.game.piece_lst.remove(self)
        self.game.piece_group.remove(self)
        piece_dict = {'queen': Queen,
                      'knight': Knight,
                      'bishop': Bishop,
                      'rook': Rook,
                      }
        #create and set new piece
        new_piece = piece_dict[piece](self.grid_pos, self.player)
        self.game.piece_lst.append(new_piece)
        self.game.piece_group.add(new_piece)
        get_tile(self.grid_pos, self.game.tile_lst).piece = new_piece
        new_piece.game = self.game
        #reset promotion state
        self.game.promoted = None
        self.game.change_turn()
        # self.game.current_turn*=-1

    def update(self):
        super().update()
        if(self.en_passant == True):
            self.image = self.image_enp
        else:
            self.image = self.image_default

class King(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'king')
        if (player == 1):
            self.image = king_white
        if (player == 2):
            self.image = king_black

        self.first_move = True

        self.castle_1_eligible = True
        self.castle_1_rook = None
        self.castle_1_valid = False

        self.castle_2_eligible = True
        self.castle_2_rook = None
        self.castle_1_valid = False

    def check_castle(self):
        #check if king has moved
        if(self.first_move==False):
            self.castle_1_eligible = False
            self.castle_2_eligible = False
        #check if rooks have moved
        if (self.castle_1_rook is None or self.castle_1_rook.first_move == False):
            self.castle_1_eligible = False
        if (self.castle_2_rook is None or self.castle_2_rook.first_move == False):
            self.castle_2_eligible = False

        if(self.castle_1_eligible):
            pass
        if(self.castle_2_eligible):
            pass

    def move(self, new_pos):
        super().move(new_pos)
        self.first_move = False

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
        self.move_lst = self.filter_moves(move_lst)
        self.check_castle()
        if(self.castle_1_valid):
            #highlight tile
            print('castle 1 valid')
            pass
        if(self.castle_2_valid):
            #highlight tile
            print('castle 2 valid')
            pass
        return self.move_lst


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
        self.move_lst = self.filter_moves(move_lst)
        return self.move_lst

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

        self.move_lst = self.filter_moves(move_lst)
        return self.move_lst

class Knight(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'knight')
        if(player == 1):
            self.image = knight_white
        if(player == 2):
            self.image = knight_black

    def get_moves(self):
        _move_lst = []
        pos1 = (self.grid_pos[0] - 1, self.grid_pos[1] - 2)
        pos2 = (self.grid_pos[0] + 1, self.grid_pos[1] - 2)
        pos3 = (self.grid_pos[0] + 2, self.grid_pos[1] - 1)
        pos4 = (self.grid_pos[0] + 2, self.grid_pos[1] + 1)
        pos5 = (self.grid_pos[0] + 1, self.grid_pos[1] + 2)
        pos6 = (self.grid_pos[0] - 1, self.grid_pos[1] + 2)
        pos7 = (self.grid_pos[0] - 2, self.grid_pos[1] + 1)
        pos8 = (self.grid_pos[0] - 2, self.grid_pos[1] - 1)
        _move_lst.append(pos1)
        _move_lst.append(pos2)
        _move_lst.append(pos3)
        _move_lst.append(pos4)
        _move_lst.append(pos5)
        _move_lst.append(pos6)
        _move_lst.append(pos7)
        _move_lst.append(pos8)

        self.move_lst = self.filter_moves(_move_lst)
        return self.move_lst

class Rook(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'rook')
        if (player == 1):
            self.image = rook_white
        if (player == 2):
            self.image = rook_black
        self.first_move = True

    def move(self, new_pos):
        super().move(new_pos)
        self.first_move = False

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

        self.move_lst = self.filter_moves(move_lst)
        return self.move_lst
