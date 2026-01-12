
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

VALID_MOVES = {"rock", "paper", "scissors", "bomb"}
VALID_RESULTS = {"user_win", "bot_win", "draw"}


class BotOutput(BaseModel):
    """Output schema for BotAgent"""
    bot_move: str = Field(
        description="Move chosen by the bot: rock, paper, scissors, or bomb"
    )
    updated_state: dict = Field(
        description="Updated state for bot bomb usage"
    )

    @field_validator("bot_move")
    @classmethod
    def validate_move(cls, v):
        if v not in VALID_MOVES:
            raise ValueError(f"Bot move must be one of {VALID_MOVES}")
        return v


# models.py
from pydantic import BaseModel
from typing import Optional

class RefereeOutput(BaseModel):
    message: Optional[str] = None
    step: Optional[str] = None
