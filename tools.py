
def update_game_state(state_updates: dict) -> dict:
    return state_updates

def validate_move(state, user_text):
    move = user_text.lower().strip()
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    updates = {}

    if move not in valid_moves:
        updates["app:is_valid_move"] = False
        updates["app:error_reason"] = "Invalid move. Allowed: rock, paper, scissors, bomb."
        return updates

    if move == "bomb" and state.get("app:user_bomb_used") == True:
        updates["app:is_valid_move"] = False
        updates["app:error_reason"] = "Bomb can only be used once."
        return updates

    # valid move
    updates["app:is_valid_move"] = True
    updates["app:user_move"] = move

    if move == "bomb":
        updates["app:user_bomb_used"] = True

    updates["app:error_reason"] = None
    return updates

def decide_winner(user_move: str, bot_move: str):
    if user_move == bot_move:
        return {"winner": "draw"}

    if user_move == "bomb" and bot_move != "bomb":
        return {"winner": "user_win"}

    if bot_move == "bomb" and user_move != "bomb":
        return {"winner": "bot_win"}

    rules = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if rules[user_move] == bot_move:
        return {"winner": "user_win"}
    else:
        return {"winner": "bot_win"}
