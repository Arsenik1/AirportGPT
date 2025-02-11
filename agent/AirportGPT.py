import asyncio
import iGA_tools
import iGA_globals
from iGA_globals import ChatState, chatState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import datetime
from typing import Literal
import json

class FlightSearchInput(BaseModel):
    search_term: str = Field(
        description="Required: Enter any search term single keyword like city name (e.g., 'London'), flight number (e.g., 'TK1234'), or airport code (e.g., 'IST')")
    isInternational: bool = Field(
        default=False,
        description="Optional: Set true for international flights, 'false' for domestic flights")
    isDeparture: bool = Field(
        default=False,
        description="Optional: Set true to search departures, 'false' to search arrivals")


async def chatController():
    tools = [
        StructuredTool(
            name="Get Flight Information",
            description="""Searches for flights at Istanbul Airport based on your criteria.
            
            Examples:
            1. For international flights from Istanbul to Berlin (This means the user is looking for flights departing from Istanbul to Berlin, internationally):
            {
              "action": "Get Flight Information",
              "action_input": {
                "search_term": "berlin",
                "isInternational": true,
                "isDeparture": 'true'
              }
            }
            
            2. For domestic arrivals from Ankara to Istanbul (This means the user is looking for flights arriving at Istanbul from Ankara, domestically):
            {
              "action": "Get Flight Information",
              "action_input": {
                "search_term": "ankara",
                "isInternational": 'false',
                "isDeparture": 'false'
              }
            }""",
            func=iGA_tools.flight_api,
            args_schema=FlightSearchInput
        )
    ]

    chatState = ChatState(
        # modelName="MFDoom/deepseek-r1-tool-calling:7b",
        modelName="qwen2.5:latest",
        num_ctx=18000,
        temperature=0.8,
        num_predict=2048,
        systemMessage=None,
        tools=tools
    )

    print("Starting chat session. Type '/bye' to end.\n")
    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "/bye":
                # Save chat history to file
                with open("chat_history.txt", "w") as f:
                    for message in chatState.messageHistory:
                        f.write(f"{message}\n")
                print("Chat history saved to chat_history.txt")
                break

            # Create a HumanMessage object and add to history
            human_message = HumanMessage(content=user_input)
            chatState.messageHistory.append(human_message)
            
            # Get response from model using agentExecutor
            # response = await chatState.structuredAgentExecutor.ainvoke({"input": user_input, "agent_scratchpad": []})
            response = await chatState.structuredAgentExecutor.ainvoke({"input": user_input})
            
            if "deepseek" in chatState.modelName:
                ai_response = response.get('output', 'No response generated')
                if not isinstance(ai_response, str):
                    ai_response = json.dumps(ai_response)
                print("Bot:", ai_response)
                chatState.messageHistory.append(AIMessage(content=ai_response))
            else:
                ai_response = response.get('output', 'No response generated')
                
                print("Bot:", ai_response)
            chatState.messageHistory.append(AIMessage(content=ai_response))
    except KeyboardInterrupt:
        print("\nChat terminated.")
        # Save chat history to file
        with open("chat_history.txt", "w") as f:
            for message in chatState.messageHistory:
                f.write(f"{message}\n")
        print("Chat history saved to chat_history.txt")
        

if __name__ == "__main__": 
    asyncio.run(chatController())
