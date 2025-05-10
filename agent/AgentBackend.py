from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uvicorn
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import iGA_globals
import iGA_tools

# Define request and response models

def createChatState():
    ret = iGA_globals.ChatState(
    modelName="qwen2.5:latest",
        num_ctx=18000, # Context length
        temperature=0.3, # Creativity
        num_predict=4096, # Maximum length of the output
        systemMessage=None,
        tools=iGA_tools.FLIGHT_TOOLS
    )
    print("DEBUG - Model Seed:", ret.seed)
    return ret

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


app = FastAPI()

# Enable CORS for your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatState = createChatState()


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    global chatState
    
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    if request.message.startswith("CLEAR_CONTEXT"):
        chatState = createChatState()
        return ChatResponse(reply="Context cleared")
    
    chatState.messageHistory.append(HumanMessage(content=request.message))
    try:
        response = await chatState.structuredAgentExecutor.ainvoke({"input": request.message})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    ai_response = response.get('output', 'No response generated')
    chatState.messageHistory.append(AIMessage(content=ai_response))
    return ChatResponse(reply=ai_response)

# Optionally, add a GET endpoint to retrieve chat history


@app.get("/history")
async def get_history():
    return {"history": [str(m) for m in chatState.messageHistory]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
