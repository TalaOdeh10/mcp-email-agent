from fastapi import FastAPI
from pydantic import BaseModel

from agent.main import EmailAgent


app = FastAPI(
    title="MCP Email AI Agent"
)


# ============================================================
# Request model
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# Global agent
# ============================================================

agent = EmailAgent()


# ============================================================
# Startup
# ============================================================

@app.on_event("startup")
async def startup():

    await agent.start()


# ============================================================
# Shutdown
# ============================================================

@app.on_event("shutdown")
async def shutdown():

    await agent.close()


# ============================================================
# Root
# ============================================================

@app.get("/")
async def root():

    return {
        "message": "MCP Email AI Agent API is running"
    }


# ============================================================
# Chat
# ============================================================

@app.post("/chat")
async def chat(request: ChatRequest):

    response = await agent.chat(
        request.message
    )

    return {
        "response": response
    }