def between_nums(num1, num2, bet_num, include=(True, False)):
    '''
    Checks if bet_num is between num1 and num2.
    :param num1: Smaller of the 2 numbers
    :param num2: Greater of the 2 numbers
    :param bet_num: The number being checked
    :param include: Tuple on whether to include the ends of the intervals
    :return:
    '''

    if(num1>num2):
        print('invalid nums')
        return False

    if(include[0]):
        if(not bet_num>=num1):
            return False
    else:
        if(not bet_num>num1):
            return False

    if (include[1]):
        if (not bet_num <= num2):
            return False
    else:
        if (not bet_num < num2):
            return False

    return True

def get_tile(pos, tile_lst):
    if (pos[0] < 0 or pos[0] >= len(tile_lst) or pos[1] < 0 or pos[1] >= len(tile_lst[0])):
        return None
    else:
        return tile_lst[pos[0]][pos[1]]
