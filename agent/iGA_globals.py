import json
import random
import re
from langchain_ollama import ChatOllama
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage
import datetime
from typing import Optional
from langchain.agents.structured_chat.base import create_structured_chat_agent
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.globals import set_verbose, set_debug
from pydantic import BaseModel

class FinalAnswer(BaseModel):
    action: str
    action_input: str


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
        
        set_verbose(True)
        # set_debug(True)

        systemMessage = f"""Current date and time is: {getCurrentDateTime()}
Your location: Istanbul/Turkey

You are the AI assistant for Istanbul Airport. When a user asks for flight information, you must use the "Get Flight Information" tool with the appropriate parameters.

Important:
- The airport is always Istanbul (IST).
- If the user asks for flights **to** another city (e.g., "flights to London"), this means flights departing **from Istanbul** to that city. In this case, set **isIstanbulOrigin** to **true**.
- If the user asks for flights **from** another city (e.g., "flights from London"), this means flights arriving **at Istanbul** from that city. In this case, set **isIstanbulOrigin** to **false**.
- Also, consider any time-related details (like "this morning" or "tonight") to filter by the scheduled time when you need to.
- Make sure to use the tools in the **correct input format** and give your **final answer** in the right template. Pay close attention to formatting.
- Be as **informative** as possible, give the user all the necessary information.
- Generate the final answer when you see **FINAL_TOOL_OUTPUT** in the tool output.

For example:
- “List me departures to London.” → Use the tool with isIstanbulOrigin = true (Istanbul is the origin).
- “I am curious if there are any flights from London this morning.” → Use the tool with isIstanbulOrigin = false (Istanbul is the destination).

**Do not** call the "Get Flight Information" tool repeatedly without new information or a different query from the user.
"""

        if "deepseek" in modelName:
            original_parse = JSONAgentOutputParser.parse

            def patched_parse(self, text: str):
                print("DEBUG - Parsing text:", text)
                cleaned = re.sub(r".*?</think>", "", text, flags=re.DOTALL)
                return original_parse(self, cleaned)

            JSONAgentOutputParser.parse = patched_parse

        # Deepseek Seeds: 
        # 4178861355 (generates json output at the end but at least works)
        # 3244298149 (works pretty good but only gives 1 flight as answer haha)
        # 1703524473 (good for asking cities or flight numbers)
        # 653840552 (good)
        
        # Qwen2.5 seeds: 
        # 2464766213
        # 1907100122
        # 3236656348
        # 3124983648
        # self.seed = random.randint(0, 2**32 - 1)  # Safe range: 0 to 4,294,967,295
        self.seed = 3124983648

        self.messageHistory = [systemMessage]
        self.modelName = modelName
        self.tools = tools
        self.model = ChatOllama(
            model=self.modelName,
            num_ctx=num_ctx,
            temperature=temperature,
            seed=self.seed,
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

        if "deepseek" in self.modelName:
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


# chatState: Optional[ChatState] = None
