import asyncio
import iGA_tools
from iGA_globals import ChatState
from iGA_globals import chatState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import Literal
import json

async def chatController():
    
    chatState = ChatState(
        modelName="llama3.1:latest",
        num_ctx=18000, # Context length
        temperature=0.3, # Creativity
        num_predict=4096, # Maximum length of the output
        systemMessage=None,
        tools=iGA_tools.FLIGHT_TOOLS
    )

    print("Starting chat session. Type '/bye' to end.\n")
    try:
        while True:
            print("DEBUG - Model Seed:", chatState.seed)
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
