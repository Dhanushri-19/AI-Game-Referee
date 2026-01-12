

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part
from google.adk.models.lite_llm import LiteLlm
from models import RefereeOutput,BotOutput
from prompt import Referee_Prompt,BotAgentPrompt
from tools import update_game_state,validate_move,decide_winner
import os
os.environ["LITELLM_DISABLE_LOGGING"] = "true"


BotAgent = LlmAgent(
    name="BotAgent",
    model=LiteLlm(model="ollama/qwen2.5:3b"),
    description="Selects a valid move for the bot and tracks bomb usage.",
    instruction=BotAgentPrompt,
    # output_key="bot_state",        # saved into session.state
    output_schema=BotOutput
)



from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

Referee_bot = LlmAgent(
    name="Referee_bot",
    model=LiteLlm(model="gemini/gemini-2.5-flash"),

    
    # model=LiteLlm(model="ollama/qwen2.5:3b"),
    description="Referee agent for Rock Paper Scissors Plus game.",
    instruction=Referee_Prompt,
    # output_key="Referee_response",
    output_schema=RefereeOutput,
    tools=[update_game_state,validate_move,decide_winner],
    # temperature=0
    sub_agents=[BotAgent]
)



print("Registered tools:")
for t in Referee_bot.tools:
    print("-", t.__name__)

async def main():

    app_name = "state_app"
    user_id = "Dhanushri Murali"
    session_id = "session1"

    session_service = InMemorySessionService()

    runner = Runner(
        agent=Referee_bot,
        app_name=app_name,
        session_service=session_service
    )

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    session.state.update({
       "app:user_move": None,
       "app:user_bomb_used": False,
       "app:bot_bomb_used": False,
       "app:is_valid_move" : None,
       "app:round_number": 0,
       "app:user_score": 0,
       "app:bot_score": 0
    })

    print(f"Initial state: {session.state}")

    while True:
      user_text = input("user: ")
      user_message = Content(parts=[Part(text=user_text)])

      for event in runner.run(
          user_id=user_id,
          session_id=session_id,
          new_message=user_message
      ):
          if event.content:
            for part in event.content.parts:

              if part.function_response:
                  tool_name = part.function_response.name
                  tool_result = part.function_response.response

                  print(f"\n🔧 Tool completed: {tool_name}")
                  print("📦 Tool returned:", tool_result)

                  # ✅ Load current session
                  session = await session_service.get_session(
                      app_name=app_name,
                      user_id=user_id,
                      session_id=session_id
                  )

                  # ✅ Merge tool result into state
                  if session.state is None:
                      session.state = {}

                  session.state.update(tool_result)

                  # ✅ Persist state back to session store
                  # await session_service.update_session(session)

                  print("✅ State persisted:", session.state)

          print("Event type:", event)
          if event.is_final_response():
              
              response_text = event.content.parts[0].text
              try:
                  import json
                  data = json.loads(response_text)
                  print("Agent:", data.get("message", response_text))
              except json.JSONDecodeError:
                  print("Agent:", response_text)
              break

      updated_session = await session_service.get_session(
          app_name=app_name,
          user_id=user_id,
          session_id=session_id
      )

      print("Current state:", updated_session.state)
      
          

    # Expected:
    # {'last_greeting': 'Hello there! How can I help you today?'}


if __name__ == "__main__":
    asyncio.run(main())
