import pygame
from tile import *
from settings import *
from utils import *

def generate_pieces(game):
    # Generate pieces
    for pawn in range(0, 8):
        pawn_w = Pawn((pawn, 1), 1)
        game.add_piece(pawn_w)
    for pawn in range(0, 8):
        pawn_b = Pawn((pawn, 6), 2)
        game.add_piece(pawn_b)

    # king_w = King((4, 7), 1)
    # game.add_piece(king_w)
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

    rook1_w = Rook((0, 7), 1)
    game.add_piece(rook1_w)
    rook2_w = Rook((7, 7), 1)
    game.add_piece(rook2_w)
    rook1_b = Rook((0, 0), 2)
    game.add_piece(rook1_b)
    rook2_b = Rook((7, 0), 2)
    game.add_piece(rook2_b)

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
        self.piece_group = pygame.sprite.Group()
        self.captures_p1 = []
        self.captures_p2 = []

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

    def add_piece(self, piece):
        self.piece_lst.append(piece)
        self.piece_group.add(piece)
        if (piece.player == 1):
            self.white_piece_lst.append(piece)
        if (piece.player == 2):
            self.black_piece_lst.append(piece)
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
        for piece in self.piece_lst:
            piece.get_moves()

    def change_turn(self):
        print('turn changed')
        if(self.current_turn == 1):
            self.current_turn = 2
        else:
            self.current_turn = 1
        for x in self.tile_lst:
            for y in x:
                y.piece_counter = []
        for piece in self.piece_lst:
            piece.get_moves()

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
