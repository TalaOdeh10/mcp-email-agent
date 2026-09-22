from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.main import EmailAgent


app = FastAPI(
    title="MCP Email AI Agent"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# ============================================================
# Frontend
# ============================================================

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)