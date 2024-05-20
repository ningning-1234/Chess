import pygame
from tile import *
from settings import *
from utils import *
from fileIO import *
from datetime import datetime

fen_to_piece = {
    'P': Pawn,
    'R': Rook,
    'N': Knight,
    'B': Bishop,
    'Q': Queen,
    'K': King,
}

# piece_to_fen = {
#     Pawn: 'P',
#     Rook: 'R',
#     Knight: 'N',
#     Bishop: 'B',
#     Queen: 'Q',
#     King: 'K',
# }

start_state = str(read_file('assets/Start_State'))

def check_FEN(fen_str):
    return True

button_images_w = {
    'rook':pygame.image.load('assets/Rook_W.png'),
    'knight':pygame.image.load('assets/Knight_W.png'),
    'bishop':pygame.image.load('assets/Bishop_W.png'),
    'queen':pygame.image.load('assets/Queen_W.png')
}
button_images_b = {
    'rook':pygame.image.load('assets/Rook_B.png'),
    'knight':pygame.image.load('assets/Knight_B.png'),
    'bishop':pygame.image.load('assets/Bishop_B.png'),
    'queen':pygame.image.load('assets/Queen_B.png')
}

class PromotionButton(pygame.sprite.Sprite):
    def __init__(self, pos, player, piece):
        super(PromotionButton, self).__init__()
        self.pos = pos
        self.player = player
        self.piece = piece
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        if(self.player == 1):
            # self.image.blit(button_images_w[piece], (0, 0))
            self.image = button_images_w[piece]
        if (self.player == 2):
            # self.image.blit(button_images_b[piece], (0, 0))
            self.image = button_images_b[piece]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.color = (100, 100, 100)

    def onclick(self, pawn):
        print('promote to ' + self.piece)
        if(type(pawn)==Pawn):
            pawn.promotion(self.piece)
        else:
            print('cannot promote')

    def update(self):
        self.draw()

    def draw(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)

bishop_w_promotion = PromotionButton((0, 0), 1, 'bishop')
knight_w_promotion = PromotionButton((TILE_SIZE*1, 0), 1, 'knight')
rook_w_promotion = PromotionButton((TILE_SIZE*2, 0), 1, 'rook')
queen_w_promotion = PromotionButton((TILE_SIZE*3, 0), 1, 'queen')
bishop_b_promotion = PromotionButton((0, 0), 2, 'bishop')
knight_b_promotion = PromotionButton((TILE_SIZE*1, 0), 2, 'knight')
rook_b_promotion = PromotionButton((TILE_SIZE*2, 0), 2, 'rook')
queen_b_promotion = PromotionButton((TILE_SIZE*3, 0), 2, 'queen')
# promotion_button_lst = [bishop_promotion,
#                         knight_promotion,
#                         rook_promotion,
#                         queen_promotion]

class ChessGame():
    def __init__(self):
        self.turn_count = 1
        self.taken_pieces = []
        self.tile_lst = []
        self.tile_group = pygame.sprite.Group()
        self.piece_lst = []
        self.white_piece_lst = []
        self.black_piece_lst = []
        self.king_b = None
        self.king_w = None

        self.piece_group = pygame.sprite.Group()
        self.captures_p1 = []
        self.captures_p2 = []
        self.board_state = ''

        #1 = white
        #2 = black
        self.current_turn = 1

        self.board_pos = (60,60)
        self.board_surface = pygame.surface.Surface((TILE_SIZE*8, TILE_SIZE*8))
        self.highlighted_tiles = []
        self.clicked = None

        self.promoted = None
        self.promotion_ui_pos_w = (180, 0)
        self.promotion_ui_surface_w = pygame.surface.Surface((240, 60))
        self.promotion_ui_surface_w.fill((80,80,80))
        self.promotion_ui_pos_b = (180, 540)
        self.promotion_ui_surface_b = pygame.surface.Surface((240, 60))
        self.promotion_ui_surface_b.fill((200,200,200))
        self.promotion_button_group_w = pygame.sprite.Group(bishop_w_promotion,
                        knight_w_promotion,
                        rook_w_promotion,
                        queen_w_promotion)
        self.promotion_button_group_b = pygame.sprite.Group(bishop_b_promotion,
                        knight_b_promotion,
                        rook_b_promotion,
                        queen_b_promotion)
        self.move_notation = []

    def add_piece(self, piece):
        self.piece_lst.append(piece)
        self.piece_group.add(piece)
        if (piece.player == 1):
            self.white_piece_lst.append(piece)
        if (piece.player == 2):
            self.black_piece_lst.append(piece)
        piece.add_piece(self)
        self.tile_lst[piece.grid_pos[0]][piece.grid_pos[1]].piece = piece

    def generate_board(self):
        # Generate grid
        for tiles_x in range(GRID_SIZE):
            self.tile_lst.append([])
            for tiles_y in range(GRID_SIZE):
                t = Tile((tiles_x, tiles_y))
                self.tile_lst[tiles_x].append(t)
                self.tile_group.add(t)

        self.king_w=None
        self.king_b=None
        global start_state
        if(not check_FEN(start_state)):
            start_state = DEFAULT_START_STATE
        txt_lst = start_state.split(' ')
        '''
        txt_lst[0]: piece placement
        txt_lst[1]: current turn
        txt_lst[2]: castling
        txt_lst[3]: enp
        txt_lst[4]: half move
        txt_lst[5]: full move
        '''
        txt_lst[0] = txt_lst[0].split('/')
        print(txt_lst)

        #temp storage for castling rooks
        castle_w_q = None
        castle_w_k = None
        castle_b_q = None
        castle_b_k = None
        row = 0
        for x in txt_lst[0]:
            column = 0
            for y in x:
                if (y.isnumeric()):
                    column = column + int(y)
                else:
                    if (y.isupper()):
                        player = 1
                    else:
                        player = 2
                    piece = fen_to_piece[y.upper()]((column, row), player)
                    self.add_piece(piece)

                    # king
                    if (y == 'K'):
                        self.king_w = piece
                        if (row != 7 or column != 4):
                            piece.first_move = False
                        #castling
                        if('K' in txt_lst[2]):
                            piece.castle_k_eligible=True
                        if('Q' in txt_lst[2]):
                            piece.castle_q_eligible=True
                    if (y == 'k'):
                        self.king_b = piece
                        if (row != 0 or column != 4):
                            piece.first_move = False
                        #castling
                        if('k' in txt_lst[2]):
                            piece.castle_k_eligible=True
                        if('q' in txt_lst[2]):
                            piece.castle_q_eligible = True

                    # pawn
                    if (y == 'P'):
                        if (row != 6):
                            piece.first_move = False
                        if (txt_lst[3] != '-'):
                            print('enp2')
                            if (notation_to_grid_pos(txt_lst[3]) == (row, column)):
                                print('enp3')
                                piece.en_passant = True
                                print(str(piece)+' enp')
                    if (y == 'p'):
                        if (row != 1):
                            piece.first_move = False
                        if (txt_lst[3] != '-'):
                            print('enp2')
                            if (notation_to_grid_pos(txt_lst[3]) == (row, column)):
                                print('enp3')
                                piece.en_passant = True
                                print(str(piece)+' enp')

                    # rook
                    if (y == 'R'):
                        #white queen side
                        if(row == 7 and column == 0 and 'Q' in txt_lst[2]):
                            castle_w_q = piece
                        #white king side
                        elif(row == 7 and column == 7 and 'K' in txt_lst[2]):
                            castle_w_k = piece
                        else:
                            piece.first_move = False
                    if (y == 'r'):
                        #black queen side
                        if(row == 0 and column == 0 and 'Q' in txt_lst[2]):
                            castle_b_q = piece
                        #black king side
                        elif(row == 0 and column == 7 and 'K' in txt_lst[2]):
                            castle_b_k = piece
                        else:
                            piece.first_move = False
                    column = column + 1
            row = row + 1
            if(self.king_w is not None):
                self.king_w.castle_q_rook = castle_w_q
                self.king_w.castle_k_rook = castle_w_k
            if(self.king_b is not None):
                self.king_b.castle_q_rook = castle_b_q
                self.king_b.castle_k_rook = castle_b_k

        if(txt_lst[1] == 'w'):
            self.current_turn = 1
        else:
            self.current_turn = 2

        self.get_board_moves(self.current_turn)

    def get_board_moves(self, turn):
        for tile_x in self.tile_lst:
            for tile in tile_x:
                tile.piece_counter = []
        for piece in self.piece_lst:
            if(piece.active):
                piece.move_lst = piece.get_moves(turn)
        if(turn==1):
            self.king_w.get_check()
        else:
            self.king_b.get_check()

    def change_turn(self):
        print('turn changed')
        if(self.current_turn == 1):
            self.current_turn = 2
        else:
            self.current_turn = 1
        for tile_x in self.tile_lst:
            for tile in tile_x:
                tile.last_piece = None
        self.get_board_moves(self.current_turn)
        self.board_to_fen()

    def save_last(self):
        for tile_x in self.tile_lst:
            for tile in tile_x:
                tile.last_piece = tile.piece

    #reset all pieces to previoius positions
    def reset_to_last(self):
        print('resetting')
        for tile_x in self.tile_lst:
            for tile in tile_x:
                tile.piece = tile.last_piece
                #reset the piece's position
                if(tile.last_piece is not None):
                    tile.last_piece.grid_pos = tile.grid_pos
                    tile.last_piece.active = True
                tile.last_piece = None
        self.get_board_moves(self.current_turn)

    def board_to_fen(self):
        '''
        txt_lst[0]: piece placement
        txt_lst[1]: current turn
        txt_lst[2]: castling
        txt_lst[3]: enp
        txt_lst[4]: half move
        txt_lst[5]: full move
        '''
        fen = ''
        empty_tile_count = 0
        enp = None
        for tile_x in range(0, len(self.tile_lst)):
            for tile in range(0, len(self.tile_lst)):
                if(get_tile((tile, tile_x), self.tile_lst).piece is not None):
                    if (empty_tile_count != 0):
                        fen = fen + str(empty_tile_count)
                        empty_tile_count = 0
                    if(type(get_tile((tile, tile_x), self.tile_lst).piece) == Pawn):
                        # print('enp')
                        if(get_tile((tile, tile_x), self.tile_lst).piece.en_passant == True):
                            enp = get_tile((tile, tile_x), self.tile_lst).grid_pos
                    fen = fen + get_tile((tile, tile_x), self.tile_lst).piece.notation
                else:
                    empty_tile_count = empty_tile_count + 1
            if (empty_tile_count != 0):
                fen = fen + str(empty_tile_count)
                empty_tile_count = 0
            if(tile_x != len(self.tile_lst)-1):
                fen = fen + '/'

        if(self.current_turn == 1):
            fen = fen + ' w '
        else:
            fen = fen + ' b '

        board_castle = False
        if (self.king_w.castle_k_eligible == True):
            fen = fen + 'K'
            board_castle = True
        if (self.king_w.castle_q_eligible == True):
            fen = fen + 'Q'
            board_castle = True
        if (self.king_b.castle_k_eligible == True):
            fen = fen + 'k'
            board_castle = True
        if (self.king_b.castle_q_eligible == True):
            fen = fen + 'q'
            board_castle = True
        if (board_castle == False):
            fen = fen + '-'

        if (enp is not None):
            fen = fen + ' ' + grid_to_notation_pos(enp[0], enp[1])
        else:
            fen = fen + ' -'

        fen = fen + ' 0'
        fen = fen + ' 1'
        print(fen)
        return fen

    def save_fen(self):
        fen = datetime.now()
        fen = fen.strftime('%m-%d-%Y, %H-%M-%S')
        moves = ''
        for move in self.move_notation:
            moves = moves + move + '\n'
        save_to_file('fen/' + str(fen), moves + self.board_to_fen())

    def update(self, events, mouse_events):
        # Convert mouse_pos to board_pos
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
                        hovered.onclick(self)
                    if(self.promoted is not None):
                        ui_pos = self.promotion_ui_pos_w
                        ui_grp = self.promotion_button_group_w
                        if (self.promoted.player == 1):
                            ui_pos = self.promotion_ui_pos_w
                            ui_grp = self.promotion_button_group_w
                        if (self.promoted.player == 2):
                            ui_pos = self.promotion_ui_pos_b
                            ui_grp = self.promotion_button_group_b
                        promotion_mouse_pos = (mouse_events['pos'][0] - ui_pos[0],
                                                   mouse_events['pos'][1] - ui_pos[1])
                        for button in ui_grp:
                            if (between_nums(button.rect.left, button.rect.right, promotion_mouse_pos[0])):
                                if (between_nums(button.rect.top, button.rect.bottom, promotion_mouse_pos[1])):
                                    button.onclick(self.promoted)
        self.promotion_button_group_w.update()
        self.promotion_button_group_b.update()
        self.tile_group.update()
        self.piece_group.update()

    def draw(self, surface):
        if(self.current_turn==1):
            surface.fill((200,200,200))
        elif(self.current_turn==2):
            surface.fill((50,50,50))
        else:
            surface.fill(BG_COLOR)
        self.tile_group.draw(self.board_surface)
        self.piece_group.draw(self.board_surface)
        surface.blit(self.board_surface,self.board_pos)
        if(self.promoted is not None):
            if(self.promoted.player == 1):
                surface.blit(self.promotion_ui_surface_w, self.promotion_ui_pos_w)
                self.promotion_button_group_w.draw(self.promotion_ui_surface_w)
            if (self.promoted.player == 2):
                surface.blit(self.promotion_ui_surface_b, self.promotion_ui_pos_b)
                self.promotion_button_group_b.draw(self.promotion_ui_surface_b)
        for piece in self.captures_p1:
            image = piece.image
            image = pygame.transform.scale(image, (30, 30))
            surface.blit(image, (15, self.captures_p1.index(piece)*image.get_height()))
        for piece in self.captures_p2:
            image = piece.image
            image = pygame.transform.scale(image, (30, 30))
            surface.blit(image, (555, WIN_HEIGHT-self.captures_p2.index(piece)*image.get_height()-30))
