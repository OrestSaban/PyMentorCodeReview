from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzer.models import CodeRequest, AnalysisReport
from analyzer.core import Analyzer

app = FastAPI(title="PyMentor Review API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = Analyzer()

@app.post("/analyze", response_model=AnalysisReport)
def analyze_code(request: CodeRequest):
    return analyzer.analyze(request.code)

@app.get("/health")
def health_check():
    return {"status": "ok"}
