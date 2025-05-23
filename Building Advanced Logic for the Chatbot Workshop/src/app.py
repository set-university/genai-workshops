from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import NavigationApp
from utils.config import Config

app = FastAPI()

navigation_app = NavigationApp(Config.MODEL_PATH)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        response = navigation_app.process_query(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)