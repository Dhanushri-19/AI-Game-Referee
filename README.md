# Referee Bot - Rock Paper Scissors Bomb Game

This project implements a Rock Paper Scissors Bomb game using AI agents. The game features a referee agent that manages the game state and a bot agent that plays against the user.

## State Model

The game state is managed through a session state dictionary with the following keys:

- `app:user_move`: The user's current move (rock, paper, scissors, bomb, or None)
- `app:user_bomb_used`: Boolean indicating if the user has used their bomb
- `app:bot_bomb_used`: Boolean indicating if the bot has used its bomb
- `app:is_valid_move`: Boolean indicating if the user's last move was valid
- `app:round_number`: Current round number
- `app:user_score`: User's total score
- `app:bot_score`: Bot's total score
- `app:error_reason`: Reason for invalid move (if applicable)

The state follows a strict state machine approach where the referee agent checks the current state to determine actions.

## Agent/Tool Design

### Agents

1. Referee Bot (Main Agent)
   - Uses Gemini 2.5 Flash model
   - Manages game flow and state transitions
   - Acts as a strict state machine based on session state
   - Has access to tools for state management and game logic

2. Bot Agent (Sub-agent)
   - Uses Qwen 2.5 3B model via Ollama
   - Responsible for selecting valid moves for the bot
   - Tracks bomb usage to ensure rules are followed

### Tools

1. `update_game_state(state_updates: dict)`: Updates the session state with provided changes
2. `validate_move(state, user_text)`: Validates user input and updates state accordingly
3. `decide_winner(user_move: str, bot_move: str)`: Determines the winner based on game rules

The referee agent uses these tools to maintain game state and enforce rules.

## Tradeoffs Made

- Model Selection: Initially tried using LiteLLM with Ollama models to avoid Gemini API rate limits (20 calls/day). However, smaller models like Qwen 1.5B had poor accuracy for complex game logic, so Gemini was used for the referee bot while keeping Qwen for the simpler bot agent task.
- Accuracy vs. Cost: Gemini provides better reasoning for the referee's complex decision-making, but the API limits necessitated a hybrid approach.
- State Management: Used a simple dictionary-based state instead of a more robust database to keep the implementation lightweight.

## What I Would Improve with More Time

- Full Gemini Implementation: Use Gemini for both agents to ensure consistent accuracy and complete the game flow properly.
- Tool Context Integration: Better utilize tool context to provide more informed decision-making for the agents.
- Before Callbacks: Implement before callbacks for handling invalid moves more gracefully, allowing for immediate feedback without breaking the flow.
- Enhanced Error Handling: Add more robust error handling and recovery mechanisms.
- Testing: Implement comprehensive unit tests for tools and agent behaviors.
- UI/UX: Add a simple web interface or improve the command-line interaction.
- Game Features: Add more advanced features like multiple rounds, statistics tracking, or different difficulty levels.
