from game_logic import create_board, print_board, check_winner, is_full
from bot import get_easy_move, get_medium_move
from network import host_game, join_game

def play_local_bot(difficulty):
    board = create_board()
    player_mark = "X"
    bot_mark = "O"
    
    while True:
        print_board(board)
        
        # Player Turn
        move = int(input("Enter your move (1-9): ")) - 1
        if board[move] != " ":
            print("Spot taken!")
            continue
        board[move] = player_mark
        
        if check_winner(board) or is_full(board): break
        
        # Bot Turn
        if difficulty == "easy":
            bot_move = get_easy_move(board)
        else:
            bot_move = get_medium_move(board, bot_mark, player_mark)
            
        board[bot_move] = bot_mark
        if check_winner(board) or is_full(board): break

    print_board(board)
    winner = check_winner(board)
    print(f"Winner: {winner}" if winner else "It's a draw!")

def main():
    print("=== CLI TIC-TAC-TOE ===")
    print("1. Play vs Bot (Easy)")
    print("2. Play vs Bot (Medium)")
    print("3. Host a Multiplayer Game")
    print("4. Join a Multiplayer Game")
    
    choice = input("Select an option (1-4): ")
    
    if choice == '1':
        play_local_bot("easy")
    elif choice == '2':
        play_local_bot("medium")
    elif choice == '3':
        conn = host_game()
        if conn:
            print("Multiplayer logic goes here! (Host plays as X)")
            conn.close()
    elif choice == '4':
        ip = input("Enter Host IP address: ")
        conn = join_game(ip)
        if conn:
            print("Multiplayer logic goes here! (Guest plays as O)")
            conn.close()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()