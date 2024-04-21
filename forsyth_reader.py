txt = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
txt_lst = txt.split(' ')
txt_lst[0] = txt_lst[0].split('/')
print(txt_lst)
piece_notation = {
    'P': 'pawn_w',
    'p': 'pawn_b',
    'R': 'rook_w',
    'r': 'rook_b',
    'N': 'knight_w',
    'n': 'knight_b',
    'B': 'bishop_w',
    'b': 'bishop_b',
    'Q': 'queen_w',
    'q': 'queen_b',
    'K': 'king_w',
    'k': 'king_b',
}
for x in txt_lst[0]:
    for y in x:
        if(y.isnumeric()):
            print('space_'+y, end=' ')
        else:
            print(piece_notation[y], end=' ')
    print()
