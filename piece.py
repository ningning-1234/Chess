import pygame.sprite
from settings import *
from utils import *

# todo
#  Put castle tiles in lst
#  Fix pawn castle problem

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
    def __init__(self, grid_pos, player, name, notation):
        super().__init__()
        self.game = None
        self.image = pawn_white
        self.rect = self.image.get_rect()
        self.grid_pos = grid_pos
        self.player = player
        if(self.player == 1):
            self.notation = notation.upper()
        if (self.player == 2):
            self.notation = notation.lower()
        self.name = name
        #whether this piece is currently on the board
        self.active = True

        self.move_lst = []

        if (player == 1):
            self.name += ' w'
        if (player == 2):
            self.name += ' b'
        # print(self)

    def __str__(self):
        return self.name + ' at ' + str(self.grid_pos)

    def captured(self, piece):
        print('captured by ' + str(piece))

    def can_move_to(self, pos, ignore_type=0, ignore_path=0):
        '''
        Check if piece can move to given position
        :param pos: the position to move to
        :param ignore_type: the types of pieces to ignore
                                0 to not ignore anything
                                1 to ignore pieces of the same type and player
                                2 to ignore pieces of the same player
                                3 to ignore all pieces
        :param ignore_path: the types of pieces to ignore in the path
                                0 to not ignore anything
                                1 to ignore pieces of opposite player in path
                                2 to ignore pieces of the same player in path
                                3 to ignore all pieces in path

        :return:
        '''
        tile_piece = get_tile(pos, self.game.tile_lst).piece
        if (ignore_type == 0):
            if tile_piece is not None:
                return False
        elif(ignore_type==1):
            if(tile_piece is not None and tile_piece.notation != self.notation):
                return False
        elif(ignore_type==2):
            if(tile_piece is not None and tile_piece.player != self.player):
                return False

        return True

    def get_moves(self, turn):
        return []

    def filter_moves(self, moves_temp, turn):
        moves = []
        for tile in moves_temp:
            t = get_tile(tile, self.game.tile_lst)
            #capture
            if (t is not None):
                if (t.piece is None or (t.piece.player != self.player and t.piece.active==True)):
                    moves.append(tile)
                if (self.player != turn):
                    t.piece_counter.append(self)
        return moves

    # check that the position a piece wants to move to is valid
    def check_valid_move(self, new_pos):
        #check that the position is in the piece's move lst
        # if(new_pos not in self.move_lst):
        #     print('not in move lst')
        #     return False
        #check there is no friendly piece on new position
        # if(get_tile(new_pos, self.game.tile_lst).piece is not None):
        #     if(get_tile(new_pos, self.game.tile_lst).piece.player == self.player):
        #         print('friendly piece')
        #         return False

        #simulate future board
        #remove piece from current tile
        self.game.tile_lst[self.grid_pos[0]][self.grid_pos[1]].piece = None
        #move to new postition
        self.grid_pos = new_pos
        new_tile = self.game.tile_lst[new_pos[0]][new_pos[1]]
        if(new_tile.piece is not None):
            new_tile.piece.active = False
        new_tile.piece = self
        if (self.player == 1):
            self.game.get_board_moves(1)
            if (self.game.king_w.check == True):
                print('white king in check, reset')
                return False
        else:
            self.game.get_board_moves(2)
            if (self.game.king_b.check == True):
                print('black king in check, reset')
                return False
        return True

    def move(self, new_pos):
        # self.game.tile_lst[self.grid_pos[0]][self.grid_pos[1]].piece = None
        # self.grid_pos = new_pos
        new_tile = self.game.tile_lst[new_pos[0]][new_pos[1]]
        if (new_tile.last_piece is not None):
            #previous piece at that tile
            p = new_tile.last_piece
            if(p.player != self.player):
                # capture
                print(str(self) + 'captured ' + str(p))
                if (self.player == 1):
                    self.game.captures_p1.append(p)
                    self.game.black_piece_lst.remove(p)
                if (self.player == 2):
                    self.game.captures_p2.append(p)
                    self.game.white_piece_lst.remove(p)
                self.game.piece_lst.remove(p)
                self.game.piece_group.remove(p)

        move_notation = self.notation.upper() + grid_to_notation_pos(self.grid_pos[0], self.grid_pos[1])
        for piece in self.game.piece_lst:
            if (piece.notation == self.notation and piece != self):
                print('same piece')
                print(new_tile.grid_pos)
                if(piece.can_move_to(new_tile.grid_pos, ignore_type=1)):
                    print('same move')
                    move_notation = 'test' + str(move_notation)
                    break
        self.game.move_notation.append(self.notation.upper() + grid_to_notation_pos(self.grid_pos[0], self.grid_pos[1]))
        print(move_notation)
        self.game.change_turn()

    def highlight_moves(self):
        move_lst = self.move_lst
        for pos in move_lst:
            t = get_tile(pos, self.game.tile_lst)
            if (t.piece is None):
                if (self.game.current_turn == self.player and
                        self.game.promoted is None):
                    if (len(t.piece_counter) != 0):
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

    def add_piece(self,game):
        self.game = game

    def update(self):
        self.rect.topleft = (self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE)

    def draw(self, surface):
        pass


class Pawn(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'pawn', 'P')
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

    def __str__(self):
        return super().__str__()+' enp:' + str(self.en_passant)+' enp cap:' + str(self.en_passant_capture)

    def get_moves(self, turn):
        self.en_passant_capture = None
        move_lst = []
        if (self.player == 1):
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
        move_lst = self.filter_moves(move_lst, turn)
        # disable enpassant
        if (self.en_passant and self.player == self.game.current_turn):
            self.en_passant = False
        # self.en_passant_capture = False
        return move_lst

    def filter_moves(self, moves_temp, turn):
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
            # movement
            if (get_tile(moves_temp[2], self.game.tile_lst).piece is not None):
                moves.append(moves_temp[2])
            # capture highlight
            # if (self.player != self.game.current_turn):
            #     get_tile(moves_temp[2], self.game.tile_lst).piece_counter.append(self)
            # en_passant
            p = get_tile((self.grid_pos[0] - 1, self.grid_pos[1]), self.game.tile_lst).piece
            if (p is not None and type(p) == Pawn):
                if (p.player != self.player and p.en_passant):
                    moves.append(moves_temp[2])
                    self.en_passant_capture = p
                    if (self.player != turn):
                        get_tile(moves_temp[2], self.game.tile_lst).piece_counter.append(self)
        if (self.player != turn and get_tile(moves_temp[2], self.game.tile_lst) is not None):
            get_tile(moves_temp[2], self.game.tile_lst).piece_counter.append(self)
        # Capture right
        if (filtered_moves[3] == True):
            if (get_tile(moves_temp[3], self.game.tile_lst).piece is not None):
                moves.append(moves_temp[3])
            # if (self.player != self.game.current_turn):
            #     get_tile(moves_temp[3], self.game.tile_lst).piece_counter.append(self)
            # en_passant
            p = get_tile((self.grid_pos[0] + 1, self.grid_pos[1]), self.game.tile_lst).piece
            if (p is not None and type(p) == Pawn):
                if (p.player != self.player and p.en_passant):
                    moves.append(moves_temp[3])
                    self.en_passant_capture = p
                    if (self.player != turn):
                        get_tile(moves_temp[3], self.game.tile_lst).piece_counter.append(self)
            if (self.player != turn and get_tile(moves_temp[3], self.game.tile_lst) is not None):
                get_tile(moves_temp[3], self.game.tile_lst).piece_counter.append(self)
        return moves

    def check_valid_move(self, new_pos):
        self.last_pos = self.grid_pos
        return super().check_valid_move(new_pos)

    def move(self, new_pos):
        # self.game.tile_lst[self.grid_pos[0]][self.grid_pos[1]].piece = None
        # set enpassant if moving 2 squares
        if (self.last_pos[1] == self.grid_pos[1] - 2 or self.last_pos[1] == self.grid_pos[1] + 2):
            self.en_passant = True

        self.grid_pos = new_pos
        new_tile = self.game.tile_lst[new_pos[0]][new_pos[1]]
        self.first_move = False

        #capturing
        if (new_tile.last_piece is not None):
            p=new_tile.last_piece
            # capture
            print('captured ' + str(p))
            if (p.player != self.player):
                if (self.player == 1):
                    self.game.captures_p1.append(p)
                if (self.player == 2):
                    self.game.captures_p2.append(p)
                self.game.piece_lst.remove(p)
                self.game.piece_group.remove(p)
        #enpassant capture
        # elif (self.en_passant_capture is not None):

        # piece to capture
        if (self.player == 1):
            p = get_tile((self.grid_pos[0], self.grid_pos[1] + 1), self.game.tile_lst).piece
            # if (p == self.en_passant_capture):
            if(type(p)==Pawn and p.player!=self.player and p.en_passant):
                self.game.captures_p1.append(p)
                print('en passant capture')
                self.game.piece_lst.remove(p)
                self.game.piece_group.remove(p)
        else:
            p = get_tile((self.grid_pos[0], self.grid_pos[1] - 1), self.game.tile_lst).piece
            # if (p == self.en_passant_capture):
            if (type(p) == Pawn and p.player != self.player and p.en_passant):
                self.game.captures_p2.append(p)
                print('en passant capture')
                self.game.piece_lst.remove(p)
                self.game.piece_group.remove(p)
        self.en_passant_capture = None

        # new_tile.piece = self
        if (self.grid_pos[1] == 0 or self.grid_pos[1] == 7):
            self.game.promoted = self
            for piece in self.game.piece_lst:
                piece.get_moves(self.game.current_turn)
            # self.game.current_turn *=-1
            # self.promotion()

        if (self.game.promoted is None):
            self.game.change_turn()
        self.game.move_notation.append(grid_to_notation_pos(self.grid_pos[0], self.grid_pos[1]))
        print(grid_to_notation_pos(self.grid_pos[0], self.grid_pos[1]))

    def promotion(self, piece='queen'):
        # remove pawn
        self.game.piece_lst.remove(self)
        self.game.piece_group.remove(self)
        piece_dict = {'queen': Queen,
                      'knight': Knight,
                      'bishop': Bishop,
                      'rook': Rook,
                      }
        # create and set new piece
        new_piece = piece_dict[piece](self.grid_pos, self.player)
        self.game.piece_lst.append(new_piece)
        self.game.piece_group.add(new_piece)
        if(self.player == 1):
            self.game.white_piece_lst.append(new_piece)
        else:
            self.game.black_piece_lst.append(new_piece)
        get_tile(self.grid_pos, self.game.tile_lst).piece = new_piece
        new_piece.game = self.game
        # reset promotion state
        self.game.promoted = None
        self.game.change_turn()
        # self.game.current_turn*=-1

    def update(self):
        super().update()
        if (self.en_passant == True):
            self.image = self.image_enp
        else:
            self.image = self.image_default


class King(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'king', 'K')
        if (player == 1):
            self.image = king_white
        if (player == 2):
            self.image = king_black

        self.check = False

        self.first_move = True

        self.castle_q_eligible = False
        self.castle_q_rook = None
        self.castle_q_tile = (2, grid_pos[1])
        self.castle_q_rook_tile = (3, grid_pos[1])
        self.castle_q_valid = False

        self.castle_k_eligible = False
        self.castle_k_rook = None
        self.castle_k_tile = (6, grid_pos[1])
        self.castle_k_rook_tile = (5, grid_pos[1])
        self.castle_k_valid = False

        self.castle_q_tiles = []
        self.castle_k_tiles = []

    def add_piece(self, game):
        super().add_piece(game)
        self.castle_q_tiles = [get_tile((self.grid_pos[0] - 1, self.grid_pos[1]), self.game.tile_lst),
                               get_tile((self.grid_pos[0] - 2, self.grid_pos[1]), self.game.tile_lst),
                               get_tile((self.grid_pos[0] - 3, self.grid_pos[1]), self.game.tile_lst)]

        self.castle_k_tiles = [get_tile((self.grid_pos[0] + 1, self.grid_pos[1]), self.game.tile_lst),
                               get_tile((self.grid_pos[0] + 2, self.grid_pos[1]), self.game.tile_lst)]
    def check_castle(self):
        print(str(self) + ' castle check')
        self.castle_q_valid = False
        self.castle_k_valid = False

        # check if king has moved
        if (self.first_move == False):
            print('king moved')
            self.castle_q_eligible = False
            self.castle_k_eligible = False
            return

        # check if rooks have moved
        if (self.castle_q_rook is None or self.castle_q_rook.first_move == False):
            print('rook1 moved')
            self.castle_q_eligible = False
        if (self.castle_k_rook is None or self.castle_k_rook.first_move == False):
            print('rook2 moved')
            self.castle_k_eligible = False

        # check if king is in check
        if(self.check==True):
            self.castle_q_valid = False
            self.castle_k_valid = False
            print('king in check')
            return

        #checking for space between king and rook
        if (self.castle_q_eligible):
            for tile in self.castle_q_tiles:
                if (tile.piece is not None or len(tile.piece_counter) > 0):
                    print('piece in way 1')
                    self.castle_q_valid = False
                    break
                else:
                    self.castle_q_valid = True
        else:
            self.castle_q_valid = False
        if (self.castle_k_eligible):
            for tile in self.castle_k_tiles:
                if (tile.piece is not None or len(tile.piece_counter) > 0):
                    print('piece in way 2')
                    self.castle_k_valid = False
                    break
                else:
                    self.castle_k_valid = True
        else:
            self.castle_k_valid = False

    def move(self, new_pos):
        self.first_move = False
        super().move(new_pos)

    def get_check(self):
        t = get_tile(self.grid_pos, self.game.tile_lst)
        if (len(t.piece_counter) > 0):
            print(t.piece_counter)
            self.check = True
            print(str(self.player) + ' in check ' + str(len(t.piece_counter)))
        else:
            self.check = False

    def get_moves(self, turn):
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
        self.check_castle()
        if (self.castle_q_valid):
            move_lst.append(self.castle_q_tile)
            print('castle 1 valid')
        if (self.castle_k_valid):
            move_lst.append(self.castle_k_tile)
            print('castle 2 valid')
        move_lst = self.filter_moves(move_lst, turn)
        return move_lst

class Queen(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'queen', 'Q')
        if (player == 1):
            self.image = queen_white
            self.notation = 'Q'
        if (player == 2):
            self.image = queen_black
            self.notation = 'q'

    def can_move_to(self, pos, ignore_type=0, ignore_path=0):
        if(super().can_move_to(pos, ignore_type, ignore_path)==False):
            return False

    def get_moves(self, turn):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1])
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
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
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
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
        move_lst = self.filter_moves(move_lst, turn)
        return move_lst


class Bishop(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'bishop', 'B')
        if (player == 1):
            self.image = bishop_white
        if (player == 2):
            self.image = bishop_black

    def can_move_to(self, pos, ignore_type=0, ignore_path=0):
        if(super().can_move_to(pos, ignore_type, ignore_path)==False):
            return False

    def get_moves(self, turn):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1] - tile)
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
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

        move_lst = self.filter_moves(move_lst, turn)
        return move_lst


class Knight(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'knight', 'N')
        if (player == 1):
            self.image = knight_white
        if (player == 2):
            self.image = knight_black

    def can_move_to(self, pos, ignore_type=0, ignore_path=0):
        if(super().can_move_to(pos, ignore_type, ignore_path)==False):
            return False


    def get_moves(self, turn):
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

        move_lst = self.filter_moves(move_lst, turn)
        return move_lst

class Rook(Piece):
    def __init__(self, grid_pos, player):
        super().__init__(grid_pos, player, 'rook', 'R')
        if (player == 1):
            self.image = rook_white
        if (player == 2):
            self.image = rook_black
        self.first_move = True

    def move(self, new_pos):
        self.first_move = False
        super().move(new_pos)

    def can_move_to(self, pos, ignore_type=0, ignore_path=0):
        if(super().can_move_to(pos, ignore_type, ignore_path)==False):
            return False

        if(pos[0]!=self.grid_pos[0] and pos[1]!=self.grid_pos[1]):
            return False

        path_to_pos = []
        #todo:
        # get the path from current pos to the given pos

        for _pos in path_to_pos:
            tile_piece = get_tile(_pos, self.game.tile_lst).piece
            if(ignore_path==0):
                if(tile_piece is not None):
                    return False
            elif(ignore_path==1):
                if(tile_piece is not None and tile_piece.player==self.player):
                    return False
            elif(ignore_path==2):
                if(tile_piece is not None and tile_piece.player!=self.player):
                    return False
        return True

    def get_moves(self, turn):
        move_lst = []
        for tile in range(1, 8):
            pos = (self.grid_pos[0] - tile, self.grid_pos[1])
            move_lst.append(pos)
            if (get_tile(pos, self.game.tile_lst) is None):
                break
            elif (get_tile(pos, self.game.tile_lst).piece is not None):
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

        move_lst = self.filter_moves(move_lst, turn)
        return move_lst
