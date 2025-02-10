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
# Import the function
from langchain.agents.structured_chat.base import create_structured_chat_agent
# Import the default parser
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools.render import render_text_description_and_args
from langchain.agents.format_scratchpad import format_log_to_str


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

        systemMessage = """Current date and time is: {current_time}
Your location: Istanbul/Turkey

You are an AI assistant helping users find flight information.

When the user asks for flight information, use the "Get Flight Information" tool to find relevant flights.
The search_term can be a city, airport code, or flight number.
isInternational should be set to True for international flights and False for domestic.
isDeparture should be set to True for departure flights and False for arrival flights.

After using the "Get Flight Information" tool, present the results to the user in a readable format.
If no flights are found, inform the user that no flights matching their criteria were found.
If flights are found, list the flight number, departure, and arrival for each flight.

Do not call the "Get Flight Information" tool repeatedly without new information or a different query from the user.
"""

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

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=self.chatHistory
        )

        if self.modelName.startswith("deepseek"):
            prompt = toolUsePrompt  # Initialize prompt here
            self.output_parser = DeppSeekOutputParser()

            tools_string = render_text_description_and_args(self.tools)
            tool_names = ", ".join([t.name for t in self.tools])

            prompt = prompt.partial(
                tools=tools_string,
                tool_names=tool_names,
            )

            llm_with_stop = self.model.bind(stop=["\nObservation"])

            base_agent = (
                RunnablePassthrough.assign(
                    agent_scratchpad=lambda x: format_log_to_str(
                        x["intermediate_steps"]),
                )
                | prompt
                | llm_with_stop
            )

            # 2. Override the output parser
            self.structuredAgent = base_agent | self.output_parser

        else:
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


class DeppSeekOutputParser(AgentOutputParser):
    """Custom parser to handle DeepSeek R1's output format."""

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            # Use a regex to capture JSON with action/action_input
            match = re.search(
                r"\{\s*\"action\"\s*:\s*\"(.*?)\",\s*\"action_input\"\s*:\s*(\{.*?\}|\[.*?\]|\".*?\")\s*\}", text, re.DOTALL)
            if match:
                # Rebuild the JSON string carefully
                rebuilt_json = f'{{"action": "{match.group(1)}", "action_input": {match.group(2)}}}'
                action_json = json.loads(rebuilt_json)
                # Return AgentAction if "action" is not "Final Answer"
                if action_json["action"] != "Final Answer":
                    return AgentAction(
                        tool=action_json["action"],
                        tool_input=action_json["action_input"],
                        log=text
                    )
                else:
                    # If "action" is "Final Answer"
                    return AgentFinish({"output": action_json["action_input"]}, text)
        except Exception as e:
            print(f"Parsing Error: {e}")
            return AgentFinish({"output": "Could not parse tool instructions."}, text)

        # Fallback: treat as a final answer
        return AgentFinish({"output": text.strip()}, text)

    @property
    def _type(self) -> str:
        return "custom"
