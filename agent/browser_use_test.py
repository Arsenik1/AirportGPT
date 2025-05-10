# import os

# Optional: Disable telemetry
# os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Optional: Set the OLLAMA host to a remote server
# os.environ["OLLAMA_HOST"] = "http://x.x.x.x:11434"

import asyncio
from browser_use import Agent, Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use.agent.views import AgentHistoryList
from langchain_ollama import ChatOllama
import iGA_tools
import iGA_globals

# TODO: Restrict URL's add: "https://docs.browser-use.com/customize/browser-settings"
# TODO: Writing custom function for flisht use case: "https://docs.browser-use.com/customize/custom-functions"
# TODO: output formatting: "https://docs.browser-use.com/customize/output-format"
async def run_search_ollama() -> AgentHistoryList:
    
    config = BrowserContextConfig(
        browser_window_size={'width': 720, 'height': 1200},
        locale='en-US',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        allowed_domains=['istairport.com', 'google.com', 'igairport.aero'],
        viewport_expansion=800
    )
    browser = Browser()
    context = BrowserContext(browser, config)
    
    model = ChatOllama(model="qwen2.5:latest", num_ctx=18500, temperature=0.85)
    
    agent = Agent(
        task="Go to 'https://www.istairport.com/en/flights/flight-info/arriving-flights/?locale=en' and tell me the status of international departure flight flight TK1853",
        # task="Do a duckduckgo search about how I can use local llm with browser-use, open the first non-ad link and summarize the content.",
        browser_context=context,
        llm=model,
        max_actions_per_step=1,
        use_vision=False,
        initial_actions=[
            {
                "go_to_url": {
                    "url": "https://www.google.com"
                }
            }
        ]
        
    )

    result = await agent.run()
    return result

async def main():
    result = await run_search_ollama()
    print("\n\n", result)


if __name__ == "__main__":
    asyncio.run(main())
