import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.browser import run_agent

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIX: correct static folder
app.mount("/static", StaticFiles(directory="backend/static"), name="static")


# Request schema
class RunAgent(BaseModel):
    url: str
    max_steps: int = 5
    goal: str = "explore"


# API endpoint
@app.post("/run-agent")
async def run_ai_agent(data: RunAgent):
    # ✅ FIX: pass goal
    result = await run_agent(data.url, data.max_steps, data.goal)
    return result