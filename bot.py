import random
from game_logic import check_winner

def get_easy_move(board):
    empty_spots = [i for i, spot in enumerate(board) if spot == " "]
    return random.choice(empty_spots) if empty_spots else None

def get_medium_move(board, bot_mark, player_mark):
    empty_spots = [i for i, spot in enumerate(board) if spot == " "]
    
    # 1. Check if Bot can win in the next move
    for spot in empty_spots:
        board_copy = list(board)
        board_copy[spot] = bot_mark
        if check_winner(board_copy) == bot_mark:
            return spot

    # 2. Check if Bot needs to block the Player from winning
    for spot in empty_spots:
        board_copy = list(board)
        board_copy[spot] = player_mark
        if check_winner(board_copy) == player_mark:
            return spot

    # 3. Otherwise, pick a random spot
    return random.choice(empty_spots) if empty_spots else None