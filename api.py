from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import your real pipeline
from orchestrator_crewai import run_with_crewai

app = FastAPI()

# Allow React frontend (localhost:3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    idea: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        # 🔥 THIS IS THE REAL CALL (CrewAI + Ollama + your agents)
        result = run_with_crewai(req.idea)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
