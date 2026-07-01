import random
import chess

print(chess.__dict__['PIECE_NAMES'])

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0  # King value is omitted as it cannot be captured
}

def evaluate_board(board):
    """Calculates the material balance of the board."""
    if board.is_checkmate():
        # If the current player is checkmated, it's a terrible position
        return -99999 if board.turn == chess.WHITE else 99999
        
    score = 0
    # Sum up values for all pieces on the board
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
        
    return score

def get_best_move(board,depth):
    """Looks 1 move ahead to find the highest-scoring move."""
    legal_moves = list(board.legal_moves)
    best_move = legal_moves[0]
    
    # White wants the highest score, Black wants the lowest score
    Moves = {}
    if board.turn == chess.WHITE:
        best_score = float('-inf')
        
        for _ in range(depth):
            for move in legal_moves:
                board.push(move)  # Simulate the move
                score = evaluate_board(board)
                board.pop()       # Undo the move
                Moves[move]=score 
        lowest_key = min(Moves, key=Moves.get)                 
        return lowest_key        
    else:
        best_score = float('inf')
        for _ in range(depth):
        
            for move in legal_moves:
                board.push(move)
                score = evaluate_board(board)
                board.pop()
                Moves[move]=score 
        highest_key = max(Moves, key=Moves.get)                 
        return highest_key
def simulate_random_game(depth):
    # Initialize a standard chess board state
    board = chess.Board()
    
    print("Starting simulation...")
    print(board)
    print("\n" + "="*20 + "\n")
    
    # Loop until the game is over (checkmate, stalemate, draw, etc.)
    while not board.is_game_over():
       move = get_best_move(board,depth)
        
        # Push the move onto the board state
       board.push(move)
        
        # Print the move and the updated board
       print(f"Move played: {move}")
       print(board)
       print("\n" + "-"*20 + "\n")
        
    print("Game Over!")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    # To run this, install the library first via: pip install python-chess
    simulate_random_game(10000)
# Example Simulation Trigger
