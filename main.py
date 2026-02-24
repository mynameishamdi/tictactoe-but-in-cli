from game_logic import create_board, print_board, check_winner, is_full
from bot import get_easy_move, get_medium_move
from network import host_game, join_game

def play_local_bot(difficulty):
    # ... (Keep your existing play_local_bot code here) ...
    board = create_board()
    player_mark = "X"
    bot_mark = "O"
    
    while True:
        print_board(board)
        
        move = int(input("Enter your move (1-9): ")) - 1
        if board[move] != " ":
            print("Spot taken!")
            continue
        board[move] = player_mark
        
        if check_winner(board) or is_full(board): break
        
        if difficulty == "easy":
            bot_move = get_easy_move(board)
        else:
            bot_move = get_medium_move(board, bot_mark, player_mark)
            
        if bot_move is not None:
            board[bot_move] = bot_mark
            
        if check_winner(board) or is_full(board): break

    print_board(board)
    winner = check_winner(board)
    print(f"Winner: {winner}" if winner else "It's a draw!")

# --- NEW MULTIPLAYER LOGIC ---
def play_multiplayer(conn, is_host):
    board = create_board()
    my_mark = "X" if is_host else "O"
    their_mark = "O" if is_host else "X"
    my_turn = is_host # Host goes first
    
    print(f"\nGame Started! You are playing as '{my_mark}'.")
    
    try:
        while True:
            print_board(board)
            
            if my_turn:
                # 1. My Turn
                while True:
                    try:
                        move = int(input("Enter your move (1-9): ")) - 1
                        if move < 0 or move > 8 or board[move] != " ":
                            print("Invalid or taken spot! Try again.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Update board and send to opponent
                board[move] = my_mark
                conn.send(str(move).encode())
                
                if check_winner(board) or is_full(board): break
                
                print("\nWaiting for opponent's move...")
                my_turn = False 
                
            else:
                # 2. Opponent's Turn
                data = conn.recv(1024).decode()
                if not data:
                    print("\nOpponent disconnected unexpectedly.")
                    break
                
                their_move = int(data)
                board[their_move] = their_mark
                
                if check_winner(board) or is_full(board): break
                
                my_turn = True

        # End of game summary
        print_board(board)
        winner = check_winner(board)
        if winner == my_mark:
            print("Congratulations! You won!")
        elif winner == their_mark:
            print("Opponent won! Better luck next time.")
        else:
            print("It's a draw!")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        conn.close()

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
            play_multiplayer(conn, is_host=True)
    elif choice == '4':
        ip = input("Enter Host IP address (e.g., 127.0.0.1 for local test): ")
        conn = join_game(ip)
        if conn:
            play_multiplayer(conn, is_host=False)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()