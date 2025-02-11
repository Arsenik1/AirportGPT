import json
import re
from langchain_ollama import ChatOllama
from langchain import hub
from langchain.agents import AgentOutputParser, AgentExecutor, create_react_agent, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.agents import AgentAction, AgentFinish
import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field  # Add this import at the top
# Import the function
from langchain.agents.structured_chat.base import create_structured_chat_agent
# Import the default parser
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools.render import render_text_description_and_args
from langchain.agents.format_scratchpad import format_log_to_str
import re
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain_ollama import ChatOllama

class ReasoningConversationBufferMemory(ConversationBufferMemory):
    async def asave_context(self, inputs, outputs):
        # Convert output to string if it isn’t already.
        output_str = outputs.get("output")
        if not isinstance(output_str, str):
            outputs["output"] = json.dumps(output_str)
        return await super().asave_context(inputs, outputs)
    
def getCurrentDateTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S - %A")


class ChatState:
    def __init__(self, modelName, num_ctx, temperature, num_predict=128, systemMessage=None, tools=None):
        # toolUsePrompt = hub.pull("hwchase17/react")
        toolUsePrompt = hub.pull("hwchase17/structured-chat-agent")
        # toolUsePrompt = hub.pull("cpatrickalves/react-chat-agent")
        # toolUsePrompt = hub.pull("hwchase17/react-chat-json")
        # toolUsePrompt = hub.pull("hwchase17/react")

        systemMessage = f"""Current date and time is: {getCurrentDateTime()}
Your location: Istanbul/Turkey

You are the AI assistant of Istanbul Airport (IST), helping users find flight information.

When the user asks for flight information, use the "Get Flight Information" tool to find relevant flights.
The search_term can be a city, airport code, or flight number.
isInternational should be set to 'true' for international flights and 'false' for domestic(Inside Turkey).
isDeparture should be set to 'true' for Istanbul departure flights and 'false' for Istanbul arrival flights.

After using the "Get Flight Information" tool, **analyze the JSON response you receive.**
**If flights are found in the response, present them to the user in a readable format, listing the flight number, departure, and arrival for each flight.**
**If no flights are found (the JSON response indicates no flights), inform the user that no flights matching their criteria were found.**
**Do not call the "Get Flight Information" tool again unless the user provides new criteria or asks a different question.**

Do not call the "Get Flight Information" tool repeatedly without new information or a different query from the user.
"""

        

        original_parse = JSONAgentOutputParser.parse

        def patched_parse(self, text: str):
            cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            return original_parse(self, cleaned)

        JSONAgentOutputParser.parse = patched_parse


        self.messageHistory = [systemMessage]
        self.modelName = modelName
        self.tools = tools
        self.model = ChatOllama(
            model=self.modelName,
            num_ctx=num_ctx,
            temperature=temperature
        )

        self.agent = create_react_agent(
            llm=self.model,
            tools=self.tools,
            prompt=toolUsePrompt,
            stop_sequence=True
        )
        self.agentExecutor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )

        self.chatHistory = ChatMessageHistory()
        self.chatHistory.add_message(SystemMessage(content=systemMessage))

        if  "deepseek" in self.modelName:
            self.memory = ReasoningConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                chat_memory=self.chatHistory
            )
        else:
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                chat_memory=self.chatHistory
            )

        self.structuredAgent = create_structured_chat_agent(
            llm=self.model,
            tools=self.tools,
            prompt=toolUsePrompt
        )

        self.structuredAgentExecutor = AgentExecutor(
            agent=self.structuredAgent,
            tools=self.tools,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )


chatState: Optional[ChatState] = None
