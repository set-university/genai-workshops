from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app import SecuritySystem

app = FastAPI(
    title="ATLAS Security System API",
    description="API for interacting with the ATLAS security system",
    version="1.0.0"
)

# Initialize security system
security_system = SecuritySystem()

class UserInput(BaseModel):
    message: str

class SecurityResponse(BaseModel):
    level: int
    message: str
    response: str
    level_up: bool
    status: str

@app.get("/")
async def root():
    return {
        "name": "ATLAS Security System",
        "status": "active",
        "current_level": security_system.current_level
    }

@app.post("/chat", response_model=SecurityResponse)
async def chat(user_input: UserInput):
    try:
        response, level_up = security_system.process_input(user_input.message)
        
        status = "ACCESS_GRANTED" if level_up else "WAITING_FOR_PASSWORD"
        
        if level_up:
            security_system.level_up()
        
        return SecurityResponse(
            level=security_system.current_level,
            message=user_input.message,
            response=response,
            level_up=level_up,
            status=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/restart")
async def restart():
    security_system.restart()
    return {
        "message": "System restarted",
        "current_level": security_system.current_level
    }

@app.get("/status")
async def get_status():
    return {
        "current_level": security_system.current_level,
        "max_level": security_system.max_level,
        "system_status": "active"
    } 