from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.agent import AIAgent

app = FastAPI()
agent = AIAgent()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        response = await agent.handle_request(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
